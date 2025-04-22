import "./MovieCard.css"
import { Detail } from "./routes/detail"
import { useNavigate } from "react-router-dom"

// This component displays a single movie card
function MovieCard({ movie }) {
    const navigate = useNavigate()

    const handleClick = () => {
      navigate(`/movies/${movie.id}`)
    }
  return (
    <div className="movie-card" onClick={handleClick}>
      {/* Movie poster placeholder */}
      <div className="movie-poster">
        <span>{movie.title.charAt(0)}</span>
      </div>

      {/* Movie details */}
      <div className="movie-details">
        <h3 className="movie-title">{movie.title}</h3>
        <div className="movie-info">
          <span className="movie-year">{movie.year}</span>
          <div className="movie-rating">
            <span className="star">★</span>
            <span>{movie.average_rating.toFixed(1)}</span>
            <span className="count">({movie.rating_count})</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default MovieCard
