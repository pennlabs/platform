from accounts.serializers import StudentSerializer


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': StudentSerializer(user.student, context={'request': request}).data
    }
