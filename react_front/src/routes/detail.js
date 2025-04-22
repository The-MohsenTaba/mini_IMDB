import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { 
  Box, 
  Heading, 
  Text, 
  HStack, 
  Button,
  useToast,
  Skeleton,
  Badge
} from "@chakra-ui/react";
import { StarIcon } from "@chakra-ui/icons";
import axios from "axios";

export default function MovieDetail() {
  const { movieID } = useParams();
  const [movie, setMovie] = useState(null);
  const [userRating, setUserRating] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const toast = useToast();

  axios.defaults.withCredentials = true;

  useEffect(() => {
    const fetchMovie = async () => {
      try {
        setIsLoading(true);
        const { data } = await axios.get(`http://localhost:8000/movies/${movieID}/`);
        
        setMovie(data);
        
        // Handle my_vote object structure
        if (data.my_vote && data.my_vote.rating) {
          setUserRating(parseFloat(data.my_vote.rating));
        } else {
          setUserRating(null);
        }

      } catch (error) {
        toast({
          title: "Error loading movie",
          description: error.message,
          status: "error",
          duration: 3000,
        });
      } finally {
        setIsLoading(false);
      }
    };

    fetchMovie();
  }, [movieID]);

  const handleRating = async (rating) => {
    try {
      await axios.post(
        `http://localhost:8000/movies/${movieID}/vote/`,
        { rating },
        { withCredentials: true }
      );
      
      // Update user rating (as object to match API format)
      setUserRating(rating);
      
      toast({
        title: "Rating submitted!",
        status: "success",
        duration: 2000,
      });
      
      // Refresh movie data
      const { data } = await axios.get(`http://localhost:8000/movies/${movieID}/`);
      setMovie(data);
      if (data.my_vote && data.my_vote.rating) {
        setUserRating(parseFloat(data.my_vote.rating));
      }

    } catch (error) {
      toast({
        title: "Failed to submit rating",
        description: error.response?.data?.message || error.message,
        status: "error",
        duration: 3000,
      });
    }
  };

  if (isLoading) return <Skeleton height="200px" />;
  if (!movie) return <Text>Movie not found</Text>;

  return (
    <Box p={4} maxW="800px" margin="0 auto">
      <Heading size="xl" mb={2}>
        {movie.title} ({movie.year})
      </Heading>

      <HStack mb={4}>
        <StarIcon color="yellow.400" />
        <Text>
          Average: {movie.average_rating.toFixed(1)} (from {movie.rating_count} ratings)
        </Text>
      </HStack>

      {userRating === null ? (
        <Box mb={6}>
          <Text mb={2}>Rate this movie:</Text>
          <HStack>
            {[1, 2, 3, 4, 5].map((star) => (
              <Button
                key={star}
                leftIcon={<StarIcon />}
                onClick={() => handleRating(star)}
                colorScheme="yellow"
                variant="outline"
              >
                {star}
              </Button>
            ))}
          </HStack>
        </Box>
      ) : (
        <Text mb={6}>Your rating: {userRating}/5</Text>
      )}

      {/* Display rating badge if available */}
      {movie.my_vote && (
        <Badge colorScheme="green" p={2} borderRadius="md">
          <HStack>
            <StarIcon />
            <Text>Your vote: {movie.my_vote.rating}</Text>
          </HStack>
        </Badge>
      )}
    </Box>
  );
}