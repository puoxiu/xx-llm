import bcrypt
print(bcrypt.__version__)       # 应输出 "4.3.0"
print(hasattr(bcrypt, "__about__"))  # 应输出 False
print(hasattr(bcrypt, "__version__"))  # 应输出 True