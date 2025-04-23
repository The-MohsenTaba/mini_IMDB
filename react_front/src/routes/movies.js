import { useState, useEffect } from "react"
import MovieCard from "../MovieCard"
import { Route, Router, Routes } from "react-router-dom"
import { Detail } from "./detail"
import { useNavigate } from "react-router-dom"
import { logout } from "../endpoints/api"

function Movies() {
  const [movies, setMovies] = useState([])
  const [filteredMovies, setFilteredMovies] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [searchQuery, setSearchQuery] = useState("")
  const [sortBy, setSortBy] = useState("title")
  const [sortDirection, setSortDirection] = useState("asc")

  const nav = useNavigate();

  useEffect(() => {
    const fetchMovies = async () => {
      try {
        setLoading(true)
        // Use your movies endpoint directly
        const response = await fetch('http://127.0.0.1:8000/movies/', {
          credentials: 'include',  // This is crucial!
          headers: {
            'Content-Type': 'application/json',
          }
        });
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }

        const data = await response.json()
        console.log("API Response:", data)

        // Handle different response formats
        let moviesArray = []
        
        if (Array.isArray(data)) {
          // If response is direct array
          moviesArray = data
        } else if (data.results) {
          // If paginated response
          moviesArray = data.results
        } else if (typeof data === 'object') {
          // If single object response, convert to array
          moviesArray = [data]
        }

        console.log("Movies array:", moviesArray)
        setMovies(moviesArray)
        setFilteredMovies(moviesArray)

      } catch (err) {
        console.error("Error fetching movies:", err)
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchMovies()
  }, [])


  useEffect(() => {
    let result = [...movies]

    // Apply search filter
    if (searchQuery) {
      result = result.filter((movie) => movie.title.toLowerCase().includes(searchQuery.toLowerCase()))
    }

    // Apply sorting
    result.sort((a, b) => {
      let comparison = 0

      // Sort based on selected field
      if (sortBy === "title") {
        comparison = a.title.localeCompare(b.title)
      } else if (sortBy === "year") {
        comparison = a.year - b.year
      } else if (sortBy === "rating") {
        comparison = a.average_rating - b.average_rating
      }

      // Reverse if descending order
      return sortDirection === "asc" ? comparison : -comparison
    })

    setFilteredMovies(result)
  }, [movies, searchQuery, sortBy, sortDirection])
  // Rest of your component code...
  // Keep all your existing filter/sort logic and JSX rendering

  
  // Handle search input change
  const handleSearchChange = (e) => {
    setSearchQuery(e.target.value)
  }
  
  // Handle sort selection change
  const handleSortChange = (e) => {
  setSortBy(e.target.value)
}

// Toggle sort direction
const toggleSortDirection = () => {
  setSortDirection(sortDirection === "asc" ? "desc" : "asc")
}

// Show loading state
if (loading) {
  return <div className="loading">Loading movies...</div>
}

// Show error state
if (error) {
  return <div className="error">{error}</div>
}
const handleLogout = async()=>{
  try{
    console.log("meow")
    const success = await logout();
    if (success){
      nav("../login/")
    }
  }catch(error){
    console.error("logout Error : ",error)
  }
}
return (
  <div className="app">
    <button onClick={handleLogout}> LogOut </button>
    <header>
      <h1>Mini IMDB</h1>
    </header>

    <div className="controls">
      {/* Search input */}
      <div className="search-container">
        <input
          type="text"
          placeholder="Search movies..."
          value={searchQuery}
          onChange={handleSearchChange}
          className="search-input"
        />
      </div>

      {/* Sort controls */}
      <div className="sort-container">
        <label>
          Sort by:
          <select value={sortBy} onChange={handleSortChange} className="sort-select">
            <option value="title">Title</option>
            <option value="year">Year</option>
            <option value="rating">Rating</option>
          </select>
        </label>

        <button onClick={toggleSortDirection} className="sort-direction-button">
          {sortDirection === "asc" ? "Ascending ↑" : "Descending ↓"}
        </button>
      </div>
    </div>

    {/* Results count */}
    <div className="results-count">
      Showing {filteredMovies.length} of {movies.length} movies
    </div>

    {/* Movie list */}
    {filteredMovies.length === 0 ? (
      <div className="no-results">
        <p>No movies found. Try a different search.</p>
      </div>
    ) : (
      <div className="movie-list">
        {filteredMovies.map((movie) => (
          <MovieCard key={movie.id} movie={movie} />
        ))}
      </div>
    )}
  </div>
)
}



export default Movies
