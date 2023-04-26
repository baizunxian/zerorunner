# import traceback
#
# from flask import Blueprint, request
# from loguru import logger
#
# from autotest.exc import codes
# from autotest.forms.form import SendMessageSchema
# from autotest.models.sys_models import Notify, User
# from autotest.services.system_service.notify_service import notify
# from autotest.utils.api import partner_success, login_verification, parse_pagination
#
# bp = Blueprint('notify', __name__, url_prefix='/api')
#
#
# @bp.route('/notifyList', methods=['POST'])
# @login_verification
# @json_required
# def notify_list():
#     parsed_data = request.json
#     user_id = parsed_data.get('user_id', None)
#     send_status = parsed_data.get('send_status', None)
#     read_status = parsed_data.get('read_status', None)
#     data = parse_pagination(Notify.get_list(user_id=user_id, send_status=send_status, read_status=read_status))
#     _result, pagination = data.get('result'), data.get('pagination')
#     _result = SendMessageSchema().dump(_result, many=True)
#     result = {
#         'rows': _result
#     }
#     result.update(pagination)
#     return partner_success(data=result)
#
#
# @bp.route('/notifyInfo', methods=['POST'])
# @login_verification
# @json_required
# def get_notify_info():
#     parsed_data = request.json
#     n_id = parsed_data.get('id', None)
#     notify_info = Notify.get(n_id)
#     if notify_info:
#         notify_info.read_status = 20
#         notify_info.save()
#     n_info = SendMessageSchema().dump(notify_info)
#     return partner_success(n_info)
#
#
# @bp.route('/sendMessage', methods=['POST'])
# @login_verification
# def send_message():
#     """
#     :return:
#     """
#     parsed_data = request.json
#     message = parsed_data.get('message', None)
#     group = parsed_data.get('group', 'notify')
#     user_ids = parsed_data.get('user_ids', [])
#     try:
#         data = notify.send_message(group=group, message=message, user_ids=user_ids)
#         return data
#     except Exception as err:
#         logger.error(traceback.format_exc())
#         return partner_success(code=codes.PARTNER_CODE_FAIL, msg=str(err))
#
#
# @bp.route('/getGroupInfo', methods=['POST'])
# @login_verification
# def get_group_info():
#     """
#     :return:
#     """
#     data = notify.get_group_info()
#     return data
