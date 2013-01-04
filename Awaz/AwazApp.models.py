# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Zaudiodata(models.Model):
    z_pk = models.IntegerField(null=True, primary_key=True, db_column=u'Z_PK', blank=True) # Field name made lowercase.
    z_ent = models.IntegerField(null=True, db_column=u'Z_ENT', blank=True) # Field name made lowercase.
    z_opt = models.IntegerField(null=True, db_column=u'Z_OPT', blank=True) # Field name made lowercase.
    zaudio_file_path = models.TextField(db_column=u'ZAUDIO_FILE_PATH', blank=True) # Field name made lowercase. This field type is a guess.
    class Meta:
        db_table = u'ZAUDIODATA'

class Zhistorydata(models.Model):
    z_pk = models.IntegerField(null=True, primary_key=True, db_column=u'Z_PK', blank=True) # Field name made lowercase.
    z_ent = models.IntegerField(null=True, db_column=u'Z_ENT', blank=True) # Field name made lowercase.
    z_opt = models.IntegerField(null=True, db_column=u'Z_OPT', blank=True) # Field name made lowercase.
    zdate = models.TextField(db_column=u'ZDATE', blank=True) # Field name made lowercase. This field type is a guess.
    zhistory = models.TextField(db_column=u'ZHISTORY', blank=True) # Field name made lowercase. This field type is a guess.
    class Meta:
        db_table = u'ZHISTORYDATA'

class Zimagedata(models.Model):
    z_pk = models.IntegerField(null=True, primary_key=True, db_column=u'Z_PK', blank=True) # Field name made lowercase.
    z_ent = models.IntegerField(null=True, db_column=u'Z_ENT', blank=True) # Field name made lowercase.
    z_opt = models.IntegerField(null=True, db_column=u'Z_OPT', blank=True) # Field name made lowercase.
    zindex = models.DecimalField(decimal_places=None, null=True, max_digits=None, db_column=u'ZINDEX', blank=True) # Field name made lowercase.
    zdirectory_path = models.TextField(db_column=u'ZDIRECTORY_PATH', blank=True) # Field name made lowercase. This field type is a guess.
    zfile_name = models.TextField(db_column=u'ZFILE_NAME', blank=True) # Field name made lowercase. This field type is a guess.
    zkey_words = models.TextField(db_column=u'ZKEY_WORDS', blank=True) # Field name made lowercase. This field type is a guess.
    class Meta:
        db_table = u'ZIMAGEDATA'

class Zpicmodedict(models.Model):
    z_pk = models.IntegerField(null=True, primary_key=True, db_column=u'Z_PK', blank=True) # Field name made lowercase.
    z_ent = models.IntegerField(null=True, db_column=u'Z_ENT', blank=True) # Field name made lowercase.
    z_opt = models.IntegerField(null=True, db_column=u'Z_OPT', blank=True) # Field name made lowercase.
    zis_enabled = models.IntegerField(null=True, db_column=u'ZIS_ENABLED', blank=True) # Field name made lowercase.
    zis_sentence_box_enabled = models.IntegerField(null=True, db_column=u'ZIS_SENTENCE_BOX_ENABLED', blank=True) # Field name made lowercase.
    zserial = models.DecimalField(decimal_places=None, null=True, max_digits=None, db_column=u'ZSERIAL', blank=True) # Field name made lowercase.
    zversion = models.DecimalField(decimal_places=None, null=True, max_digits=None, db_column=u'ZVERSION', blank=True) # Field name made lowercase.
    zaudio_data = models.TextField(db_column=u'ZAUDIO_DATA', blank=True) # Field name made lowercase. This field type is a guess.
    zcategory_or_template = models.TextField(db_column=u'ZCATEGORY_OR_TEMPLATE', blank=True) # Field name made lowercase. This field type is a guess.
    zcolor = models.TextField(db_column=u'ZCOLOR', blank=True) # Field name made lowercase. This field type is a guess.
    zidentifier = models.TextField(db_column=u'ZIDENTIFIER', blank=True) # Field name made lowercase. This field type is a guess.
    zparent_id = models.TextField(db_column=u'ZPARENT_ID', blank=True) # Field name made lowercase. This field type is a guess.
    zpicture = models.TextField(db_column=u'ZPICTURE', blank=True) # Field name made lowercase. This field type is a guess.
    ztag_name = models.TextField(db_column=u'ZTAG_NAME', blank=True) # Field name made lowercase. This field type is a guess.
    class Meta:
        db_table = u'ZPICMODEDICT'

class Zpredictiondict(models.Model):
    z_pk = models.IntegerField(null=True, primary_key=True, db_column=u'Z_PK', blank=True) # Field name made lowercase.
    z_ent = models.IntegerField(null=True, db_column=u'Z_ENT', blank=True) # Field name made lowercase.
    z_opt = models.IntegerField(null=True, db_column=u'Z_OPT', blank=True) # Field name made lowercase.
    zfrequency = models.DecimalField(decimal_places=None, null=True, max_digits=None, db_column=u'ZFREQUENCY', blank=True) # Field name made lowercase.
    zparent = models.TextField(db_column=u'ZPARENT', blank=True) # Field name made lowercase. This field type is a guess.
    zprediction = models.TextField(db_column=u'ZPREDICTION', blank=True) # Field name made lowercase. This field type is a guess.
    class Meta:
        db_table = u'ZPREDICTIONDICT'

class Zpronounciationdata(models.Model):
    z_pk = models.IntegerField(null=True, primary_key=True, db_column=u'Z_PK', blank=True) # Field name made lowercase.
    z_ent = models.IntegerField(null=True, db_column=u'Z_ENT', blank=True) # Field name made lowercase.
    z_opt = models.IntegerField(null=True, db_column=u'Z_OPT', blank=True) # Field name made lowercase.
    zactual = models.TextField(db_column=u'ZACTUAL', blank=True) # Field name made lowercase. This field type is a guess.
    zspoken = models.TextField(db_column=u'ZSPOKEN', blank=True) # Field name made lowercase. This field type is a guess.
    class Meta:
        db_table = u'ZPRONOUNCIATIONDATA'

class Zquickaccessdata(models.Model):
    z_pk = models.IntegerField(null=True, primary_key=True, db_column=u'Z_PK', blank=True) # Field name made lowercase.
    z_ent = models.IntegerField(null=True, db_column=u'Z_ENT', blank=True) # Field name made lowercase.
    z_opt = models.IntegerField(null=True, db_column=u'Z_OPT', blank=True) # Field name made lowercase.
    zkey = models.TextField(db_column=u'ZKEY', blank=True) # Field name made lowercase. This field type is a guess.
    zquick_text = models.TextField(db_column=u'ZQUICK_TEXT', blank=True) # Field name made lowercase. This field type is a guess.
    class Meta:
        db_table = u'ZQUICKACCESSDATA'

class Zsettingsdata(models.Model):
    z_pk = models.IntegerField(null=True, primary_key=True, db_column=u'Z_PK', blank=True) # Field name made lowercase.
    z_ent = models.IntegerField(null=True, db_column=u'Z_ENT', blank=True) # Field name made lowercase.
    z_opt = models.IntegerField(null=True, db_column=u'Z_OPT', blank=True) # Field name made lowercase.
    zaccesshighlightdelay = models.IntegerField(null=True, db_column=u'ZACCESSHIGHLIGHTDELAY', blank=True) # Field name made lowercase.
    zaudiospeakactionkeys = models.IntegerField(null=True, db_column=u'ZAUDIOSPEAKACTIONKEYS', blank=True) # Field name made lowercase.
    zaudiospeakonselection = models.IntegerField(null=True, db_column=u'ZAUDIOSPEAKONSELECTION', blank=True) # Field name made lowercase.
    zpicmodeaddshortcut = models.IntegerField(null=True, db_column=u'ZPICMODEADDSHORTCUT', blank=True) # Field name made lowercase.
    zpicmodeautohome = models.IntegerField(null=True, db_column=u'ZPICMODEAUTOHOME', blank=True) # Field name made lowercase.
    zpicmodecaptionsize = models.IntegerField(null=True, db_column=u'ZPICMODECAPTIONSIZE', blank=True) # Field name made lowercase.
    zpicmodeenlargeimage = models.IntegerField(null=True, db_column=u'ZPICMODEENLARGEIMAGE', blank=True) # Field name made lowercase.
    zpicmodemsgbox = models.IntegerField(null=True, db_column=u'ZPICMODEMSGBOX', blank=True) # Field name made lowercase.
    zpicmodemsgboxpictures = models.IntegerField(null=True, db_column=u'ZPICMODEMSGBOXPICTURES', blank=True) # Field name made lowercase.
    ztextmodepredictionpictures = models.IntegerField(null=True, db_column=u'ZTEXTMODEPREDICTIONPICTURES', blank=True) # Field name made lowercase.
    ztextmodequickresponse = models.IntegerField(null=True, db_column=u'ZTEXTMODEQUICKRESPONSE', blank=True) # Field name made lowercase.
    zaudiospeed = models.TextField(db_column=u'ZAUDIOSPEED', blank=True) # Field name made lowercase. This field type is a guess.
    zaudiovoice = models.TextField(db_column=u'ZAUDIOVOICE', blank=True) # Field name made lowercase. This field type is a guess.
    zgenstartingscreen = models.TextField(db_column=u'ZGENSTARTINGSCREEN', blank=True) # Field name made lowercase. This field type is a guess.
    zidentifier = models.TextField(db_column=u'ZIDENTIFIER', blank=True) # Field name made lowercase. This field type is a guess.
    zpassword = models.TextField(db_column=u'ZPASSWORD', blank=True) # Field name made lowercase. This field type is a guess.
    zpicmodesize = models.TextField(db_column=u'ZPICMODESIZE', blank=True) # Field name made lowercase. This field type is a guess.
    zpicmodestartingparentid = models.TextField(db_column=u'ZPICMODESTARTINGPARENTID', blank=True) # Field name made lowercase. This field type is a guess.
    ztextmodelayout = models.TextField(db_column=u'ZTEXTMODELAYOUT', blank=True) # Field name made lowercase. This field type is a guess.
    ztextmodesize = models.TextField(db_column=u'ZTEXTMODESIZE', blank=True) # Field name made lowercase. This field type is a guess.
    class Meta:
        db_table = u'ZSETTINGSDATA'

class Zworddata(models.Model):
    z_pk = models.IntegerField(null=True, primary_key=True, db_column=u'Z_PK', blank=True) # Field name made lowercase.
    z_ent = models.IntegerField(null=True, db_column=u'Z_ENT', blank=True) # Field name made lowercase.
    z_opt = models.IntegerField(null=True, db_column=u'Z_OPT', blank=True) # Field name made lowercase.
    zfrequency = models.DecimalField(decimal_places=None, null=True, max_digits=None, db_column=u'ZFREQUENCY', blank=True) # Field name made lowercase.
    zchildren = models.TextField(db_column=u'ZCHILDREN', blank=True) # Field name made lowercase. This field type is a guess.
    zparent = models.TextField(db_column=u'ZPARENT', blank=True) # Field name made lowercase. This field type is a guess.
    zword = models.TextField(db_column=u'ZWORD', blank=True) # Field name made lowercase. This field type is a guess.
    class Meta:
        db_table = u'ZWORDDATA'

class ZMetadata(models.Model):
    z_version = models.IntegerField(null=True, primary_key=True, db_column=u'Z_VERSION', blank=True) # Field name made lowercase.
    z_uuid = models.CharField(max_length=255, db_column=u'Z_UUID', blank=True) # Field name made lowercase.
    z_plist = models.TextField(db_column=u'Z_PLIST', blank=True) # Field name made lowercase. This field type is a guess.
    class Meta:
        db_table = u'Z_METADATA'

class ZPrimarykey(models.Model):
    z_ent = models.IntegerField(null=True, primary_key=True, db_column=u'Z_ENT', blank=True) # Field name made lowercase.
    z_name = models.TextField(db_column=u'Z_NAME', blank=True) # Field name made lowercase. This field type is a guess.
    z_super = models.IntegerField(null=True, db_column=u'Z_SUPER', blank=True) # Field name made lowercase.
    z_max = models.IntegerField(null=True, db_column=u'Z_MAX', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'Z_PRIMARYKEY'

