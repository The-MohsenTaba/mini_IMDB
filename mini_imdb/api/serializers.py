from rest_framework import serializers
from .models import*


class VoteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model=Vote
        fields = ["rating",'user']
        extra_kwargs={
            'rating' : {'min_value':0 ,'max_value': 5 }
        }
        

class UserSerializer (serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["username"]
class MovieSerializer(serializers.ModelSerializer):
    my_vote=serializers.SerializerMethodField()
    class Meta:
        model=Movie
        fields='__all__'
        read_only_fields=('average_rating','rating_count')

    def get_my_vote(self,obj):
        request= self.context.get('request')
        if request and request.user.is_authenticated:
            vote = obj.vote_set.filter(user=request.user).first()
            return VoteSerializer(vote).data if vote else None
        return None