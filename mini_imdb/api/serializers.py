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


class MongoRatingSerializer(serializers.Serializer):
    user = serializers.HiddenField(default = serializers.CurrentUserDefault())
    movie = serializers.CharField()
    rating = serializers.FloatField( min_value = 0 , max_value =5)

    def create(self, validated_data):
        movie_name = validated_data.pop("movie")
        validated_data['movie'] = MongoMovie.objects.get(title = movie_name)
        user_name = validated_data.pop("user")
        validated_data['user']=str(user_name)
        rate= MongoVote(**validated_data)
        rate.save()
        return rate
    
    def update(self, instance, validated_data):
        for attr , value in validated_data.items():
            setattr(instance,attr,value)
        instance.save()
        return instance
    
    def to_representation(self, instance):
        return {
            'movie' :{
             'title': instance.movie.title,
             'year': instance.movie.year,
            },
                
            'your rating' : instance.rating,
        }


# since drf ui does not support list and cict inputs , you can only add movies via api services
class MongoMovieSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    title = serializers.CharField()
    year = serializers.IntegerField()
    average_rating=serializers.FloatField(read_only = True)

    genere=serializers.ChoiceField(choices=["Action",
                                                    "Comedy",
                                                    "Drama",
                                                    "Horror",
                                                    "Romance",
                                                    "Biography",
                                                    "Sci-fi",
                                                    "Thriller"])
    
    rating_count = serializers.IntegerField(read_only=True)
    directors = serializers.ListField(
        child=serializers.CharField(),write_only = True
    )
    actors = serializers.ListField(
        child = serializers.CharField(),write_only = True
    )


    def create(self, validated_data):
        # delete  list of string ids we recieved from our data to variables
        directors_ids = validated_data.pop('directors')
        actors_ids = validated_data.pop('actors')
        # store documents related to those ids in our data
        validated_data['directors'] = [MongoPerson.objects.get(id=did) for did in directors_ids]
        validated_data['actors'] = [MongoPerson.objects.get(id=aid) for aid in actors_ids]
        return MongoMovie(**validated_data).save()
    
    def update(self, instance, validated_data):
        for attr , value in validated_data.items():
             # if the updated fied was director or actors , we need to refrence whole document for them 
             if attr in ['directors', 'actors']:
                refs = [MongoPerson.objects.get(id=i) for i in value]
                setattr(instance, attr, refs)
             else:
                setattr(instance, attr, value)
        instance.save()
        return instance
    
    def to_representation(self, instance):
        return {
            'id': str(instance.id),
            'title' : instance.title,
            'year' : instance.year,
            'average_rating' : instance.average_rating,
            'rating_count' : instance.rating_count,
            'genere' : str(instance.genere),
            'directors': [ f"{p.first_name} {p.last_name}"for p in instance.directors],
             'actors': [ f"{p.first_name} {p.last_name}"for p in instance.actors],
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