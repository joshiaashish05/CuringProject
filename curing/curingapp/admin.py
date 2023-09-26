from django.contrib import admin
from .models import CustomUser, Project_Master, Site_Master, Structural_Element, Transaction_Concreting, Schedule_Curing


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('User_ID', 'username', 'Email', 'Contact_no', 'Project', 'Site', 'is_user', 'is_Administrator')
    list_filter = ('is_user', 'is_Administrator')
    search_fields = ('username', 'Email')
    ordering = ('User_ID',)

@admin.register(Project_Master)
class ProjectMasterAdmin(admin.ModelAdmin):
    list_display = ('Project_ID', 'Project_Name')

@admin.register(Site_Master)
class SiteMasterAdmin(admin.ModelAdmin):
    list_display = ('Site_ID', 'Site_Name', 'Project')

@admin.register(Structural_Element)
class StructuralElementAdmin(admin.ModelAdmin):
    list_display = ('Structural_Element_ID', 'Structural_Element', 'No_Of_Days', 'Frequency','Time_Bet_TwoCuring')

@admin.register(Transaction_Concreting)
class TransactionConcretingAdmin(admin.ModelAdmin):
    list_display = ('User','Transaction_Concreting_ID', 'Project', 'Site', 'Structural_Element', 'Schedule_Date_and_Time')

@admin.register(Schedule_Curing)
class ScheduleOFCuringAdmin(admin.ModelAdmin):
    list_display = ('Schedule_Curing_ID', 'Project', 'Site', 'Structural_Element', 'Schedule_Date_and_Time','Image_Of_Curing','Status')
