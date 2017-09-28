# -*- coding: utf-8 -*-
import maya.cmds as mc
from BaseCheck import BaseCheck
from miraLibs.pipeLibs import pipeFile


controls = ["Main", "FKExtraToes_R", "FKToes_R", "FKExtraHip_R", "FKHip_R", "FKExtraKnee_R", "FKKnee_R",
            "FKExtraAnkle_R",
            "FKAnkle_R", "FKExtraHip_L", "FKHip_L", "FKExtraKnee_L", "FKKnee_L", "FKExtraAnkle_L", "FKAnkle_L",
            "FKExtraWrist2_R",
            "FKWrist2_R", "FKExtraThumbFinger1_R", "FKThumbFinger1_R", "FKExtraThumbFinger2_R", "FKThumbFinger2_R",
            "FKExtraThumbFinger3_R", "FKThumbFinger3_R", "FKExtraIndexFinger5_R", "FKIndexFinger5_R", "FKHead_M",
            "FKExtraJaw_M", "FKJaw_M", "FKExtraEye_R", "FKEye_R", "FKExtraEye_L", "FKEye_L", "FKExtraScapula_L",
            "FKScapula_L", "FKExtraRoot_M", "FKRoot_M", "HipSwinger_M",
            "FKExtraSpine1_M", "FKSpine1_M", "FKExtraChest_M", "FKChest_M", "FKExtraToes_L", "FKToes_L",
            "FKExtraWrist2_L",
            "FKWrist2_L", "FKExtraThumbFinger1_L", "FKThumbFinger1_L",
            "FKExtraThumbFinger2_L", "FKThumbFinger2_L", "FKExtraThumbFinger3_L", "FKThumbFinger3_L",
            "FKExtraIndexFinger5_L", "FKIndexFinger5_L", "FKExtraIndexFinger1_L",
            "FKIndexFinger1_L", "FKExtraIndexFinger2_L", "FKIndexFinger2_L", "FKExtraIndexFinger3_L",
            "FKIndexFinger3_L",
            "FKExtraMiddleFinger5_L", "FKMiddleFinger5_L",
            "FKExtraMiddleFinger1_L", "FKMiddleFinger1_L", "FKExtraMiddleFinger2_L", "FKMiddleFinger2_L",
            "FKExtraMiddleFinger3_L", "FKMiddleFinger3_L", "FKExtraCup_L", "FKCup_L",
            "FKExtraRingFinger5_L", "FKRingFinger5_L", "FKExtraRingFinger1_L", "FKRingFinger1_L",
            "FKExtraRingFinger2_L",
            "FKRingFinger2_L", "FKExtraRingFinger3_L", "FKRingFinger3_L",
            "FKExtraPinkyFinger5_L", "FKPinkyFinger5_L", "FKExtraPinkyFinger1_L", "FKPinkyFinger1_L",
            "FKExtraPinkyFinger2_L", "FKPinkyFinger2_L", "FKExtraPinkyFinger3_L", "FKPinkyFinger3_L",
            "FKExtraShoulder_L", "FKShoulder_L", "FKExtraElbow_L", "FKElbow_L", "FKExtraWrist_L", "FKWrist_L",
            "IKExtraSpine1_M", "IKSpine1_M", "IKExtraSpine2_M", "IKSpine2_M", "IKExtraSpine3_M",
            "IKSpine3_M", "IKExtraLeg_R", "IKLeg_R", "RollExtraHeel_R", "RollHeel_R", "RollExtraToesEnd_R",
            "RollToesEnd_R", "RollExtraToes_R", "RollToes_R", "PoleExtraLeg_R", "PoleLeg_R", "IKExtraArm_R",
            "IKArm_R", "PoleExtraArm_R", "PoleArm_R", "IKExtraLeg_L", "IKLeg_L", "RollExtraHeel_L", "RollHeel_L",
            "RollExtraToesEnd_L", "RollToesEnd_L", "RollExtraToes_L", "RollToes_L", "PoleExtraLeg_L",
            "PoleLeg_L", "IKExtraArm_L", "IKArm_L", "PoleExtraArm_L", "PoleArm_L", "FKIKLeg_R", "FKIKArm_R",
            "FKIKSpine_M",
            "FKIKLeg_L", "FKIKArm_L", "BendExtraKnee1_R", "BendKnee1_R", "BendExtraKnee2_R",
            "BendKnee2_R", "BendExtraHip1_R", "BendHip1_R", "BendExtraHip2_R", "BendHip2_R", "BendExtraElbow1_R",
            "BendElbow1_R", "BendExtraElbow2_R", "BendElbow2_R", "BendExtraShoulder1_R", "BendShoulder1_R",
            "BendExtraShoulder2_R", "BendShoulder2_R", "BendExtraKnee1_L", "BendKnee1_L", "BendExtraKnee2_L",
            "BendKnee2_L", "BendExtraHip1_L", "BendHip1_L", "BendExtraHip2_L", "BendHip2_L", "BendExtraElbow1_L",
            "BendElbow1_L", "BendExtraElbow2_L", "BendElbow2_L", "BendExtraShoulder1_L", "BendShoulder1_L",
            "BendExtraShoulder2_L", "BendShoulder2_L", "AimEye_M", "AimEye_R", "AimEye_L", "RootExtraX_M", "RootX_M",
            "Fingers_L", "Fingers_R", "FKExtraIndexFinger1_R", "FKIndexFinger1_R", "FKExtraIndexFinger2_R",
            "FKIndexFinger2_R", "FKExtraIndexFinger3_R", "FKIndexFinger3_R", "FKExtraMiddleFinger5_R",
            "FKMiddleFinger5_R",
            "FKExtraMiddleFinger1_R", "FKMiddleFinger1_R", "FKExtraMiddleFinger2_R", "FKMiddleFinger2_R",
            "FKExtraMiddleFinger3_R", "FKMiddleFinger3_R", "FKExtraCup_R", "FKCup_R", "FKExtraRingFinger5_R",
            "FKRingFinger5_R",
            "FKExtraRingFinger1_R", "FKRingFinger1_R", "FKExtraRingFinger2_R", "FKRingFinger2_R",
            "FKExtraRingFinger3_R",
            "FKRingFinger3_R", "FKExtraPinkyFinger5_R", "FKPinkyFinger5_R", "FKExtraPinkyFinger1_R", "FKPinkyFinger1_R",
            "FKExtraPinkyFinger2_R", "FKPinkyFinger2_R", "FKExtraPinkyFinger3_R", "FKPinkyFinger3_R",
            "FKExtraShoulder_R",
            "FKShoulder_R", "FKExtraElbow_R", "FKElbow_R", "FKExtraWrist_R", "FKWrist_R",
            "FKExtraScapula_R", "FKScapula_R", "FKExtraNeck_M", "FKNeck_M", "FKExtraHead_M", "Grp_Main", "Master_Ctl",
            "Fly_ctl"]


class Check(BaseCheck):

    def run(self):
        context = pipeFile.PathDetails.parse_path()
        if context.asset_type == "Character":
            self.error_list = self.get_unexist()
            if self.error_list:
                self.fail_check(u"有些控制器不存在")
            else:
                self.pass_check(u"所有控制器均存在")
        else:
            self.pass_check(u"非角色不检查此项")

    @staticmethod
    def get_unexist():
        un_exists = [ctrl for ctrl in controls if not mc.objExists(ctrl)]
        return un_exists
