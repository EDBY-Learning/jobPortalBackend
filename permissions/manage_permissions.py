def get_custom_permissions(data):
        try:
            # return permission_classes depending on `action` 
            return [permission() for permission in data.permission_classes_by_action[data.action]]
        except KeyError: 
            # action is not set return default permission_classes
            return [permission() for permission in data.permission_classes]