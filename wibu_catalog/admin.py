from django.contrib import admin
from .models import Order, OrderItems, Product

class OrderItemsInline(admin.TabularInline):
    model = OrderItems
    extra = 1
    readonly_fields = ('pid', 'quantity', 'buyPrice')
    fields = ('pid', 'quantity', 'buyPrice')
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('pid', 'quantity', 'buyPrice')
        return self.readonly_fields

class OrderAdmin(admin.ModelAdmin):
    list_display = ('oid', 'orderDate', 'status', 'uid')  # Hiển thị thông tin cơ bản
    list_filter = ('status', 'orderDate', 'uid')  # Lọc theo trạng thái, ngày đặt hàng, và người dùng
    search_fields = ('oid', 'uid__username')  # Tìm kiếm theo số đơn hàng và tên người dùng
    list_per_page = 20  # Phân trang, hiển thị 20 đơn hàng mỗi trang
    inlines = [OrderItemsInline]  # Hiển thị mặt hàng trong đơn hàng

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Có thể tùy chỉnh queryset nếu cần
        return queryset

    def save_model(self, request, obj, form, change):
        # Cập nhật thông tin đơn hàng và trạng thái
        super().save_model(request, obj, form, change)

    def get_field_display(self, obj):
        return f"Số đơn hàng: {obj.oid} - Ngày đặt hàng: {obj.orderDate} - Trạng thái: {obj.status} - Người dùng: {obj.uid.username}"
    
    fieldsets = (
        (None, {
            'fields': ('oid', 'orderDate', 'status', 'uid'),
            'description': 'Thông tin cơ bản về đơn hàng'
        }),
    )

class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ('oid', 'product_name', 'quantity', 'buyPrice')  # Hiển thị thông tin mặt hàng
    list_filter = ('oid', 'pid')  # Lọc theo số đơn hàng và sản phẩm
    search_fields = ('oid__oid', 'pid__name')  # Tìm kiếm theo số đơn hàng và tên sản phẩm

    def product_name(self, obj):
        return obj.pid.name
    product_name.short_description = 'Tên sản phẩm'

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('pid', 'quantity', 'buyPrice')
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        # Cập nhật mặt hàng trong đơn hàng
        super().save_model(request, obj, form, change)
    
    def get_field_display(self, obj):
        return f"Sản phẩm: {obj.pid.name} - Số lượng: {obj.quantity} - Giá mua: {obj.buyPrice}"

    fieldsets = (
        (None, {
            'fields': ('oid', 'pid', 'quantity', 'buyPrice'),
            'description': 'Thông tin chi tiết về mặt hàng trong đơn hàng'
        }),
    )

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItems, OrderItemsAdmin)
