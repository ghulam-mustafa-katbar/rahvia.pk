from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role_badge', 'consent_badge', 'is_staff', 'date_joined')
    list_filter = ('role', 'parent_consent_granted', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name', 'parent_guardian_email')
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number', 'role')}),
        ('Parental / Guardian Consent (PDPA Compliance)', {'fields': ('parent_guardian_name', 'parent_guardian_email', 'parent_guardian_phone', 'parent_consent_granted', 'parent_consent_date', 'parent_consent_ip')}),
        ('Permissions & Access', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Audit Timestamps', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'role', 'first_name', 'last_name'),
        }),
    )

    def role_badge(self, obj):
        colors = {
            'ADMIN': ('#dcfce7', '#15803d', '#bbf7d0'),
            'COUNSELOR': ('#f3e8ff', '#7e22ce', '#e9d5ff'),
            'STUDENT': ('#e0f2fe', '#0369a1', '#bae6fd'),
        }
        bg, text, border = colors.get(obj.role, ('#f1f5f9', '#475569', '#cbd5e1'))
        return format_html(
            '<span style="background:{}; color:{}; border:1px solid {}; padding:3px 8px; border-radius:6px; font-size:0.75rem; font-weight:700;">{}</span>',
            bg, text, border, obj.get_role_display()
        )
    role_badge.short_description = 'Role'

    def consent_badge(self, obj):
        if obj.parent_consent_granted:
            return format_html('<span style="color:#16a34a; font-weight:700;">✓ Verified</span>')
        return format_html('<span style="color:#94a3b8; font-weight:600;">— Pending</span>')
    consent_badge.short_description = 'Parent Consent'
