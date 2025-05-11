from rest_framework import serializers
from .models import*

# NoSQL serializers 


class MongoPersonSerializer(serializers.Serializer):
    id = serializers.CharField(read_only= True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    def create(self, validated_data):
        return MongoPerson(**validated_data).save()
    
    def update(self, instance, validated_data):
        for attr , value in validated_data.items():
            setattr(instance,attr,value)
        instance.save()
        return instance
    
    def to_representation(self, instance):
        return {
            'id':str(instance.id),
            'first_name': instance.first_name,
            'last_name': instance.last_name
        }


class MongoMovieSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    title = serializers.CharField()
    year = serializers.IntegerField()
    average_rating=serializers.FloatField()


    def create(self, validated_data):
        return MongoMovie(**validated_data).save()
    
    def update(self, instance, validated_data):
        for attr , value in validated_data.items():
            setattr(instance,attr,value)
        instance.save()
        return instance
    
    def to_representation(self, instance):
        return {
            'id': str(instance.id),
            'title' : instance.title,
            'year' : instance.year,
            'average_rating' : instance.average_rating
        }





# SQL serializers

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
class MyVoteSerializer(serializers.ModelSerializer):
    movie = serializers.SerializerMethodField()
    user=UserSerializer()
    def get_movie (self,obj):
        my_movies= obj.movie
        return MovieSerializer(my_movies).data
    class Meta:
        model=Vote
        fields = ["rating","user","movie"]

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
    
class UserRegister(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user