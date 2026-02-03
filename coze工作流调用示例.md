——————————————————————————————————coze请求配置————————————————————————————————————————

执行工作流
post  https://api.coze.cn/v1/workflow/run
权限点: Workflow.run
执行已发布的工作流。
——————
Header
token
扣子 API 通过访问令牌进行 API 请求的鉴权。生成方式可以参考鉴权方式
cztei_qpASkUbr7zsVk9qRbDa9naaTDGNyL9dzCSlyPSqlNdPooFY5I4OJQtZGBDzOeM54j
___
Body params
-
workflow_id
待执行的 Workflow ID，此工作流应已发布。
进入 Workflow 编排页面，在页面 URL 中，workflow 参数后的数字就是 Workflow ID。例如 https://www.coze.com/work_flow?space_id=42463***&workflow_id=73505836754923***，Workflow ID 为 73505836754923***。
收起
示例：73664689170551*****
7601786439168229386
——————
parameters
工作流开始节点的输入参数及取值，你可以在指定工作流的编排页面查看参数列表。
如果工作流输入参数为 Image 等类型的文件，你可以传入文件 URL 或调用上传文件 API 获取 file_id 后传入 file_id。示例：
上传文件并传入 file_id：
单个文件示例："parameters": { "image": "{\"file_id\":\"1122334455\"}" }
文件数组示例："parameters": { "image": [ "{\"file_id\":\"1122334455\"}" ] }。
传入文件 URL：
“parameters” :{"input":"请总结图片内容", "image": "https://example.com/tos-cn-i-mdko3gqilj/example.png" }
收起
示例：{"image": "{\"file_id\":\"1122334455\"}","user_name":"George"}

——————
bot_id
需要关联的智能体 ID。 部分工作流执行时需要指定关联的智能体，例如存在数据库节点、变量节点等节点的工作流。
![Image](https://p9-arcosite.byteimg.com/tos-cn-i-goo7wpa0wc/55746fa5540b488ea83a79064a223500~tplv-goo7wpa0wc-image.image =300x)
进入智能体的开发页面，开发页面 URL 中 bot 参数后的数字就是智能体 ID。例如 https://www.coze.com/space/341****/bot/73428668*****，Bot ID 为 73428668*****。
确保调用该接口使用的令牌开通了此智能体所在空间的权限。
确保该智能体已发布为 API 服务。

示例：73428668*****
——————
ext
用于指定一些额外的字段，以 Map [String][String] 格式传入。例如某些插件会隐式用到的经纬度等字段。
目前仅支持以下字段：
latitude：String 类型，表示纬度。
longitude：String 类型，表示经度。
user_id：String 类型，表示用户 ID。

示例：{"latitude":"116.404","longitude":"39.915","user_id":"12345"}
key_1
——————
app_id
工作流所在的应用 ID。
你可以通过应用的业务编排页面 URL 中获取应用 ID，也就是 URL 中 project-ide 参数后的一串字符，例如 https://www.coze.cncom/space/739174157340921****/project-ide/743996105122521****/workflow/744102227704147**** 中，应用的 ID 为 743996105122521****。
仅运行扣子应用中的工作流时，才需要设置 app_id。智能体绑定的工作流、空间资源库中的工作流无需设置 app_id。
展开全部
示例：749081945898306****
——————
workflow_version
工作流的版本号，仅当运行的工作流属于资源库工作流时有效。未指定版本号时默认执行最新版本的工作流。
收起
示例：v0.0.5
——————
connector_id
渠道 ID，用于配置该工作流在什么渠道执行。
————————————————————————————————————————————————————————————————————
———————————————————————## 返回参数说明———————————————————————————————

batch_index
当前节点在批处理节点中的执行次数。
第一次执行时值为 0。
仅当节点为批处理节点，且未嵌套子工作流时，才会返回该参数。
展开全部
示例：3
code
调用状态码。0 表示调用成功，其他值表示调用失败，你可以通过 msg 字段判断详细的错误原因。
展开全部
content
流式输出的消息内容。
示例：什么小明要带一把尺子去看电影？
debug_url
工作流试运行调试页面。访问此页面可查看每个工作流节点的运行结果、输入输出等信息。
debug_url 的访问有效期为 7 天，过期后将无法访问。
展开全部
示例：https://www.coze.cn/work_flow?execute_id=743104097880585****&space_id=730976060439760****&workflow_id=742963539464539****
detail
error_code
调用状态码。
0 表示调用成功。
其他值表示调用失败。你可以通过 error_message 字段判断详细的错误原因。
展开全部
error_message
状态信息。API 调用失败时可通过此字段查看详细错误信息。
event
当前流式返回的数据包事件。包括以下类型：
Message：工作流节点输出消息，例如输出节点、结束节点的输出消息。可以在 data 中查看具体的消息内容。
Error：报错。可以在 data 中查看 error_code 和 error_message，排查问题。
Done：结束。表示工作流执行结束，此时 data 为空。
Interrupt：中断。表示工作流中断，此时 data 字段中包含具体的中断信息。
展开全部
示例：Message
ext
额外字段。
id
此消息在接口响应中的事件 ID。以 0 为开始。
示例：1
interrupt_data
loop_index
当前节点在循环节点中的循环次数。
第一次循环时值为 0。
仅当节点为循环节点，且未嵌套子工作流时，才会返回该参数。
展开全部
示例：2
msg
状态信息。API 调用失败时可通过此字段查看详细错误信息。
状态码为 0 时，msg 默认为空。
展开全部
示例：""
node_execute_uuid
节点每次执行的 ID，用于追踪和识别工作流中特定节点的单次执行情况。
示例：78923456777*****
node_id
输出消息的节点 ID。
示例：900001
node_is_finish
当前消息是否为此节点的最后一个数据包。
示例：true
node_seq_id
此消息在节点中的消息 ID，从 0 开始计数，例如输出节点的第 5 条消息。
示例：0
node_title
输出消息的节点名称，例如输出节点、结束节点。
示例：Message
sub_execute_id
子工作流执行的 ID。
示例：743104097880585****
usage
——————————————————————————————————————————————————
————————————————调用示例——————————————————————————
"""
This example describes how to use the workflow interface to stream chat.
"""

import os
# Our official coze sdk for Python [cozepy](https://github.com/coze-dev/coze-py)
from cozepy import COZE_CN_BASE_URL

# Get an access_token through personal access token or oauth.
coze_api_token = 'cztei_qpASkUbr7zsVk9qRbDa9naaTDGNyL9dzCSlyPSqlNdPooFY5I4OJQtZGBDzOeM54j'
# The default access is api.coze.com, but if you need to access api.coze.cn,
# please use base_url to configure the api endpoint to access
coze_api_base = COZE_CN_BASE_URL

from cozepy import Coze, TokenAuth, Stream, WorkflowEvent, WorkflowEventType  # noqa

# Init the Coze client through the access_token.
coze = Coze(auth=TokenAuth(token=coze_api_token), base_url=coze_api_base)

# Create a workflow instance in Coze, copy the last number from the web link as the workflow's ID.
workflow_id = '7601786439168229386'


# The stream interface will return an iterator of WorkflowEvent. Developers should iterate
# through this iterator to obtain WorkflowEvent and handle them separately according to
# the type of WorkflowEvent.
def handle_workflow_iterator(stream: Stream[WorkflowEvent]):
    for event in stream:
        if event.event == WorkflowEventType.MESSAGE:
            print("got message", event.message)
        elif event.event == WorkflowEventType.ERROR:
            print("got error", event.error)
        elif event.event == WorkflowEventType.INTERRUPT:
            handle_workflow_iterator(
                coze.workflows.runs.resume(
                    workflow_id=workflow_id,
                    event_id=event.interrupt.interrupt_data.event_id,
                    resume_data="hey",
                    interrupt_type=event.interrupt.interrupt_data.type,
                )
            )


handle_workflow_iterator(
    coze.workflows.runs.stream(
        workflow_id=workflow_id,
    )
)
——————————————————————————————————————————————————————
——————————————————————文件上传示例——————————————————————
上传文件
post  https://api.coze.cn/v1/files/upload
权限点: Account.uploadFile/Connector.uploadFile
调用接口上传文件到扣子编程。​
接口说明​
消息中无法直接使用本地文件，创建消息或对话前，需要先调用此接口上传本地文件到扣子编程。上传文件后，你可以在消息中通过指定 file_id 的方式在多模态内容中直接使用此文件。此接口上传的文件可用于发起对话等 API 中传入文件等多模态内容。使用方式可参考 object_string object 。​
使用限制​
​
限制​
说明​
文件大小​
该 API 允许上传的最大文件大小为 512 MB。然而，在与智能体对话时，实际可使用的文件大小取决于智能体的模型版本。​
上传方式​
必须使用 multipart/form-data 方式上传文件。​
有效期​
普通上传的文件将保存在扣子编程服务端，有效期为 3 个月。​
若上传的文件被用作扣子头像，则永久有效。​
使用限制​
上传到扣子编程的文件仅限本账号查看或使用。​
调用此接口上传文件只能获得文件的 file_id，如需获取文件的 URL，建议将文件上传到专业的存储工具中。​
不支持下载已上传的文件。用户仅可在对话、工作流、端插件、RTC 和 WebSocket 中通过 file.id 访问和使用文件。​
API 流控​
个人版：10 QPS。​
企业版：20 QPS。​
​
支持的文件格式​
​
文件类型​
支持的格式​
文档​
DOC、DOCX、XLS、XLSX、PPT、PPTX、PDF、Numbers、CSV​
文本文件​
CPP、PY、JAVA、C ​
图片​
JPG、JPG2、PNG、GIF、WEBP、HEIC、HEIF、BMP、PCD、TIFF​
音频​
WAV、MP3、FLAC、M4A、AAC、OGG、WMA、MIDI​
视频​
MP4、AVI、MOV、3GP、3GPP、FLV、WEBM、WMV、RMVB、M4V、MKV ​
压缩文件​
RAR、ZIP、7Z、GZ、GZIP、BZ2​
​
​
Header
--
token
扣子 API 通过访问令牌进行 API 请求的鉴权。生成方式可以参考鉴权方式
token=cztei_qpASkUbr7zsVk9qRbDa9naaTDGNyL9dzCSlyPSqlNdPooFY5I4OJQtZGBDzOeM54j
--
Body params
file
需要上传的文件