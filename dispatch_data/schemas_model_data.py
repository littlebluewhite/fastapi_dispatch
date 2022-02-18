import dispatch_schemas.task_schemas as task_schemas
import dispatch_schemas.reply_schemas as reply_schemas
import dispatch_schemas.confirm_schemas as confirm_schemas
import dispatch_schemas.status_schemas as status_schemas
import dispatch_schemas.level_schemas as level_schemas
import dispatch_schemas.ack_method_schemas as ack_method_schemas
import dispatch_schemas.template_schemas as template_schemas

schemas_model_dict = {
    "DispatchTask": task_schemas.DispatchTask,
    "DispatchReply": reply_schemas.DispatchReply,
    "DispatchConfirm": confirm_schemas.DispatchConfirm,
    "DispatchStatus": status_schemas.DispatchStatus,
    "DispatchLevel": level_schemas.DispatchLevel,
    "DispatchAckMethod": ack_method_schemas.DispatchAckMethod,
    "DispatchTemplate": template_schemas.DispatchTemplate
}
