# Tencent is pleased to support the open source community by making TNN available.
#
# Copyright (C) 2020 THL A29 Limited, a Tencent company. All rights reserved.
#
# Licensed under the BSD 3-Clause License (the "License"); you may not use this file except
# in compliance with the License. You may obtain a copy of the License at
#
# https://opensource.org/licenses/BSD-3-Clause
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

from utils import cmd
from utils import checker
from . import align_model
import os


def convert(onnx_path, output_dir=None, version="v1.0", optimize=True, half=False, align=False,
            input_path=None, refer_path=None):
    """
    执行 onnx 转换为 tnn 的转换指令
    :parameter:
          onnx_path:    需要转换的 onnx 文件的路径
          output_path:  生成的 tnn 文件的路径
          version:      转换模型的版本号
          optimize:     是否需要对模型进行优化,默认是需要进行优化
          halt:         是否需要转为 FP16 的模型,减小模型的大小
    :return return_code
    :exception 执行超时
    """
    proto_suffix = '.tnnproto'
    model_suffix = '.tnnmodel'
    command = "python3 onnx2tnn.py " + onnx_path
    command = command + " -version=v1.0"
    checker.check_file_exist(onnx_path)
    if optimize is True:
        command = command + " -optimize=1"
    else:
        command = command + " -optimize=0"
    if half is True:
        command = command + " -half=1"
    else:
        command = command + " -half=0"

    if output_dir is None:
        output_dir = os.path.dirname(onnx_path)
    checker.check_file_exist(output_dir)
    command = command + " -o " + output_dir
    print("the onnx2tnn command:" + command)
    work_dir = "../onnx2tnn/onnx-converter/"
    result = cmd.run(command, work_dir=work_dir)
    if result == 0:
        print("onnx2tnn succeed!")
    else:
        print("onnx2tnn failed!")
    onnx_base_name = os.path.basename(onnx_path)

    if align is True:
        if optimize is True:
            tnn_proto_name = onnx_base_name[:-len('.onnx')] + '.opt' + proto_suffix
            tnn_model_name = onnx_base_name[:-len('.onnx')] + '.opt' + model_suffix
        else:
            tnn_proto_name = onnx_base_name[:-len('.onnx')] + proto_suffix
            tnn_model_name = onnx_base_name[:-len('.onnx')] + model_suffix
        tnn_proto_path = os.path.join(output_dir, tnn_proto_name)
        tnn_model_path = os.path.join(output_dir, tnn_model_name)
        align_model.align_model(onnx_path, tnn_proto_path, tnn_model_path, input_path, refer_path)
