from django import template

register = template.Library()

@register.filter
def format_price(value):
    try:
        value = int(value)
        if value < 1000:
            return f"{value}.000 VNĐ"
        else:
            thousands = value * 1000  # Nhân 1000 để đạt được giá trị thực tế
            return f"{thousands:,} VNĐ".replace(",", ".")
    except (ValueError, TypeError):
        return value  # Trả về giá trị gốc nếu không phải số
