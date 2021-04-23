def check_password_length(password):
    if len(password) < 8:
            raise serializers.ValidationError("Password length must be atleast 8!")
    return password