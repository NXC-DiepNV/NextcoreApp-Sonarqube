from unfold.admin import ModelAdmin


class CoreAdmin(ModelAdmin):
    compressed_fields = False

    # Warning message when user tries to leave the page with unsaved form
    warn_unsaved_form = True

    list_fullwidth = True

    # Set to False, to enable filter as "sidebar"
    list_filter_sheet = False

    # Position horizontal scrollbar in changelist at the top
    list_horizontal_scrollbar_top = False

    # Disable select all action in changelist
    list_disable_select_all = True

    # Disable/Enable submit button in filter
    list_filter_submit = True

    exclude = ['deleted_at']

    def get_queryset(self, request):
        # Get record with condition deleted_at = NULL
        return super().get_queryset(request).filter(deleted_at__isnull=True)
