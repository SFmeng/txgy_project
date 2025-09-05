"""
请求日志中间件
"""
import logging
import time
import json
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse

logger = logging.getLogger('apps')


class RequestLoggingMiddleware(MiddlewareMixin):
    """请求日志中间件"""
    
    def process_request(self, request):
        """处理请求开始"""
        request.start_time = time.time()
        
        # 记录请求信息
        logger.info(f"Request started: {request.method} {request.path}")
        
        # 记录请求参数（排除敏感信息）
        if request.method == 'POST':
            try:
                body = json.loads(request.body.decode('utf-8'))
                # 过滤敏感字段
                sensitive_fields = ['password', 'token', 'secret']
                filtered_body = {
                    k: '***' if k.lower() in sensitive_fields else v 
                    for k, v in body.items()
                }
                logger.debug(f"Request body: {filtered_body}")
            except (json.JSONDecodeError, UnicodeDecodeError):
                logger.debug("Request body: [binary data]")
    
    def process_response(self, request, response):
        """处理响应"""
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            
            # 记录响应信息
            logger.info(
                f"Request completed: {request.method} {request.path} "
                f"- Status: {response.status_code} - Duration: {duration:.3f}s"
            )
            
            # 记录慢请求
            if duration > 2.0:  # 超过2秒的请求
                logger.warning(
                    f"Slow request detected: {request.method} {request.path} "
                    f"- Duration: {duration:.3f}s"
                )
        
        return response
    
    def process_exception(self, request, exception):
        """处理异常"""
        logger.error(
            f"Request exception: {request.method} {request.path} "
            f"- Exception: {str(exception)}",
            exc_info=True
        )
        
        # 返回统一的错误响应
        return JsonResponse({
            'code': 500,
            'message': '服务器内部错误',
            'timestamp': time.time()
        }, status=500)
