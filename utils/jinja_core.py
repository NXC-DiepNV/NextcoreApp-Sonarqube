class JinjaCore:
    @staticmethod
    def viet_nam_dong_format(value):
        try:
            return f"{value:,.0f} VND"  # Định dạng số với dấu phẩy và thêm đơn vị VND
        except (ValueError, TypeError):
            return value

    @staticmethod
    def integer_priority_format(value):
        if isinstance(value, float) and value.is_integer():
            return int(value)
        return value