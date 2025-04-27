import "../MovieCard.css"
import { useEffect, useState } from "react";
import axios from "axios";
import { useAuth } from "../contexts/useAuth";
import { Spinner } from "@chakra-ui/react";
axios.defaults.withCredentials = true;

function Votes() {
  const [votes, setVotes] = useState([]);
  const { isAuthenticated, loading } = useAuth();

  useEffect(() => {
    const fetchRatings = async () => {
      try {
        // First make a GET request to ensure cookies are set
        await axios.get('http://localhost:8000/', { withCredentials: true });
        
        // Then make the logout request
        const response = await axios.get(
            'http://localhost:8000/my-ratings/',
            {
                withCredentials: true,
                headers: {
                    'Content-Type': 'application/json',
                }
            }
          );
        const data = response.data;
        let ratingsArray = [];

        if (Array.isArray(data)) {
          ratingsArray = data;
        } else if (typeof data === "object") {
          ratingsArray = [data];
        }

        setVotes(ratingsArray);
      } catch (error) {
        console.error("Error fetching ratings: ", error);
      }
    };

    if (!loading && isAuthenticated) {
      fetchRatings();
    }

  }, [loading, isAuthenticated]);

  if (loading) return <Spinner size="xl" />;

  return (
    <div className="movie-list">
      {votes.map((rating, idx) => (
        <div key={idx}>
          <div className="movie-poster">
            <span>{rating.movie.title.charAt(0)}</span>
          </div>
          <h2>{rating.movie.title} ({rating.movie.year})</h2>
          <p>Rating: {rating.rating}/5</p>
          <p>By: {rating.user.username}</p>
        </div>
      ))}
    </div>
  );
}

export default Votes;
