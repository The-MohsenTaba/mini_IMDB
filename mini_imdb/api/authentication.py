from rest_framework_simplejwt.authentication import JWTAuthentication

# class CookiesJWTAuthentication(JWTAuthentication):
#     def authenticate(self, request):
#         access_token=request.COOKIES.get('access_token')

#         if not access_token :
#             print("meowwww")
#             return None
        
#         validated_token=self.get_validated_token(access_token)
#         try:
#             user=self.get_user(validated_token)
#         except:
#             print('ooooooooooooooooooo')
#             return None
#         print(user,validated_token)
#         return(user,validated_token)

class CookiesJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        print("Incoming cookies:", request.COOKIES)  # Debugging
        
        # First try to get token from cookie
        access_token = request.COOKIES.get('access_token')
        
        # Fallback to Authorization header for API clients
        if not access_token:
            header = self.get_header(request)
            if header:
                access_token = self.get_raw_token(header)
        
        if not access_token:
            print("No access token found in cookies or headers")
            return None
            
        try:
            validated_token = self.get_validated_token(access_token)
            user = self.get_user(validated_token)
            print(f"Authenticated user: {user}")
            return (user, validated_token)
        except Exception as e:
            print(f"Token validation failed: {str(e)}")
            return None