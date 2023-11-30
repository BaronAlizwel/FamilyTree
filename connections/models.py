from django.db import models
from users.models import CustomUser

class Connection(models.Model):
    # Relationship types
    FATHER = 'FAT'
    MOTHER = 'MOT'
    SON = 'SON'
    DAUGHTER = 'DAU'
    SIBLING = 'SIB'
    SPOUSE = 'SPO'
    GRANDFATHER = 'GF'
    GRANDMOTHER = 'GM'
    GRANDSON = 'GS'
    GRANDDAUGHTER = 'GD'
    UNCLE = 'UNC'
    AUNT = 'AUN'
    COUSIN = 'COU'
    NEPHEW = 'NEP'
    NIECE = 'NIE'
    FATHER_IN_LAW = 'FIL'
    MOTHER_IN_LAW = 'MIL'
    BROTHER_IN_LAW = 'BIL'
    SISTER_IN_LAW = 'SIL'
    SON_IN_LAW = 'SIL'
    DAUGHTER_IN_LAW = 'DIL'
    ADOPTIVE_FATHER = 'AFAT'
    ADOPTIVE_MOTHER = 'AMOT'
    ADOPTED_SON = 'ASON'
    ADOPTED_DAUGHTER = 'ADAU'
    ADOPTED_SIBLING = 'ASIB'
    ADOPTED_GRANDFATHER = 'AGF'
    ADOPTED_GRANDMOTHER = 'AGM'
    ADOPTED_GRANDSON = 'AGS'
    ADOPTED_GRANDDAUGHTER = 'AGD'

    RELATIONSHIP_CHOICES = [
        (FATHER, 'Father'),
        (MOTHER, 'Mother'),
        (SON, 'Son'),
        (DAUGHTER, 'Daughter'),
        (SIBLING, 'Sibling'),
        (SPOUSE, 'Spouse'),
        (GRANDFATHER, 'Grandfather'),
        (GRANDMOTHER, 'Grandmother'),
        (GRANDSON, 'Grandson'),
        (GRANDDAUGHTER, 'Granddaughter'),
        (UNCLE, 'Uncle'),
        (AUNT, 'Aunt'),
        (COUSIN, 'Cousin'),
        (NEPHEW, 'Nephew'),
        (NIECE, 'Niece'),
        (FATHER_IN_LAW, 'Father-in-law'),
        (MOTHER_IN_LAW, 'Mother-in-law'),
        (BROTHER_IN_LAW, 'Brother-in-law'),
        (SISTER_IN_LAW, 'Sister-in-law'),
        (SON_IN_LAW, 'Son-in-law'),
        (DAUGHTER_IN_LAW, 'Daughter-in-law'),
        (ADOPTIVE_FATHER, 'Adoptive Father'),
        (ADOPTIVE_MOTHER, 'Adoptive Mother'),
        (ADOPTED_SON, 'Adopted Son'),
        (ADOPTED_DAUGHTER, 'Adopted Daughter'),
        (ADOPTED_SIBLING, 'Adopted Sibling'),
        (ADOPTED_GRANDFATHER, 'Adopted Grandfather'),
        (ADOPTED_GRANDMOTHER, 'Adopted Grandmother'),
        (ADOPTED_GRANDSON, 'Adopted Grandson'),
        (ADOPTED_GRANDDAUGHTER, 'Adopted Granddaughter'),
    ]

    from_user = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL, related_name='connections')
    to_user = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL, related_name='related_to')
    relationship_type = models.CharField(max_length=4, choices=RELATIONSHIP_CHOICES)
    relationship_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.from_user.username} - {self.to_user.username} ({self.get_relationship_type_display()})'



class ConnectionRequest(models.Model):
    PENDING = 'PEN'
    ACCEPTED = 'ACC'
    REJECTED = 'REJ'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    ]

    from_user = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL, related_name='sent_requests')
    to_user = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL, related_name='received_requests')
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['from_user', 'to_user']

    def __str__(self):
        return f'{self.from_user.username} -> {self.to_user.username} ({self.get_status_display()})'

