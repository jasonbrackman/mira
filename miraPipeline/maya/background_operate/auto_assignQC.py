# -*- coding: utf-8 -*-
from miraLibs.pipeLibs.pipeDb import sql_api
from miraLibs.pipeLibs.pipeDb import get_members
from miraLibs.pipeLibs.wiseUC import wiseUC
from miraLibs.deadlineLibs import submitDeadlineCommand
import time,getpass


class auto_assignQC:
    def __init__(self, project_name=None, task_id=None,logger=None):
        self.project_name = project_name
        self.task_id = task_id
        self.db = sql_api.SqlApi(self.project_name)
        self.user_dict = get_members.JRF_staff_DB('JRF_baseInfo', 'staff').getAll()
        self.logger = logger

    def get_QC_dict(self):
        context_qcer_data = self.db.getQCConfig()
        if context_qcer_data:
            all_QC_dict = eval(context_qcer_data)
            task_department = self.db.getAssetByTaskId(self.task_id)['assetDepartment']
            return all_QC_dict[task_department]
        else:
            return
    def send_to_persons(self,sender,receiver_list,title,content,url):
        for _rec in receiver_list:
            wiseUC.send_person_msg(sender.encode('utf-8'),_rec,title,content,url,self.logger)


    def get_QCer_list_by_order(self,QC_dict,order):
        if not QC_dict:
            return
        QC_tar_list = []
        for key in QC_dict.keys():
            tmp_dict = QC_dict[key]
            if tmp_dict['order'] == order:
                QC_tar_list = tmp_dict['qcer']
        if QC_tar_list:
            return [self.user_dict[i.split('_')[0]]['domainname'] for i in QC_tar_list]
        else:
            return

    def first_assign(self):
        if not self.task_id:
            return
        QC_dict = self.get_QC_dict()
        QC_tar_list = self.get_QCer_list_by_order(QC_dict,0)
        if QC_tar_list:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            arg_dict = {'taskId':self.task_id, 'taskQCSubmitTime': current_time, "QCStep": 0}
            self.db.submitToQC(arg_dict)

            tar_dict = {'taskId':self.task_id,'QCerList':QC_tar_list}
            self.db.assignQC(tar_dict)

            # QCer_chinese_list = self.db.getChineseNameListByDomainNameList(QC_tar_list)
            self.send_to_persons(u'admin',QC_tar_list,u'你有新的QC任务',u'你有新的QC任务，任务号为%s'%(self.task_id),'')
        else :
            self.submitTaskToDeadline()


    def check_and_assign(self,QC_id):
        # current_taskId = self.db.getTaskIdByTaskQCId(QC_id)
        maker_list = self.db.getStaffByTaskId(self.task_id)['taskMakerName']
        # maker_chinese_list = self.db.getChineseNameListByDomainNameList(maker_list)
        # print maker_chinese_list

        QC_status = self.db.getAllQCStatusByTaskQCId(QC_id)
        if QC_status == '2':
            # pass
            # This status means some QC status are retake
            self.send_to_persons(u'admin',maker_list,u'任务未通过',u'你的任务未通过QC,任务号为%s,请自行查看详细信息'%(self.task_id),'')
        elif QC_status == '1':
            # This status means some QC status are waited
            print 'wait for QC'
            return

        elif QC_status == '0':

            # This status means that all QC status are approved, need to release this task
            print 'approve'


            QC_dict = self.get_QC_dict()
            current_QC_step = self.db.getQCStepByTaskQCId(QC_id)
            QCer_list = self.get_QCer_list_by_order(QC_dict,current_QC_step+1)
            if QCer_list:
                # QCer_chinese_list = self.db.getChineseNameListByDomainNameList(QCer_list)
                submit_QC_dict ={'taskId':self.task_id,'taskQCSubmitTime':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),'QCStep':current_QC_step+1}
                new_QC_dict = {'taskId':self.task_id,'QCerList':QCer_list}
                self.db.submitToQC(submit_QC_dict)
                self.db.assignQC(new_QC_dict)
                self.send_to_persons(u'admin',QCer_list,u'你有新的QC任务',u'你有新的QC任务，任务号为%s'%(self.task_id),'')
            else:
                self.submitTaskToDeadline()

    def submitTaskToDeadline(self):
        print 'can release'
        deadline_job_name = 'releaseTask_%s_%s'%(self.task_id,time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()))
        deadline_log_path = 'W:/%s/log/release/%s.txt'%(self.project_name,deadline_job_name)
        release_python_script = r'Z:\mira\miraScripts\pipeTools\background_operate\auto_release.py'
        argv = '%s %s %s'%(self.project_name,self.task_id,deadline_log_path)
        submitter = u'pipemanager'
        tar_name = u'pipemanager'
        print 'ready for submit'
        submitDeadlineCommand.submit_python_job(deadline_job_name,release_python_script,argv,submitter,tar_name)


    def get_task_type(self):
        task_dict = self.db.getAssetByTaskId(self.task_id)
        print task_dict['mdl']



if __name__ == '__main__':
    aa = auto_assignQC('sct',268)
    #aa.first_assign()
    aa.check_and_assign(230)