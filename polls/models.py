
from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
import hashlib
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)

    def gravatar_url(self):
        return "http://www.gravatar.com/avatar/%s?s=50" % hashlib.md5(self.user.email).hexdigest()


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    creator = models.ForeignKey(User, null=True)
    tags = TaggableManager()

    def __unicode__(self):
        return self.question

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.choice_text


class Comment(models.Model):
    poll = models.ForeignKey(Poll)
    user = models.ForeignKey(User)
    comment_date = models.DateTimeField(auto_now_add=True)
    comment_text = models.TextField(max_length=500)

    def __unicode__(self):
        return self.current_text


class Vote(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.ForeignKey(Choice)
    ip = models.GenericIPAddressField()
    date = models.DateTimeField('date voted',auto_now_add=True)
   
