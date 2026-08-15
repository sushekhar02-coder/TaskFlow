
# TaskFlow

TaskFlow is a full-stack task management application with a FastAPI backend, SQLAlchemy/SQLite database, frontend dashboard, algorithm-based sorting and searching, benchmarking, and an AI-style Quick Add feature.

## Features

- Create tasks
- Edit tasks
- Delete tasks
- Set task priority
- Set task due dates
- Quick Add tasks using natural-language descriptions
- Automatic priority detection
- Automatic due-date detection
- Algorithm-based searching
- Algorithm-based sorting
- Algorithm correctness checks
- Algorithm benchmarking
- SQLite database
- FastAPI backend
- Frontend dashboard
- CORS configuration
- Request logging middleware

## Tech Stack

### Backend
- Python
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite

### Frontend
- React
- Vite
- JavaScript
- CSS

### Algorithms
- Insertion Sort
- Binary Search
- Linear Search

## Project Structure

```text
TaskFlow/
│
├── backend/
│   ├── main.py
│   ├── quick_add.py
│   ├── models.py
│   ├── schemas.py
│   ├── algorithms.py
│   ├── database.py
│   └── ...
│
├── frontend/
│   ├── package.json
│   ├── src/
│   └── ...
│
├── benchmark_results.json
├── check_algorithms.py
├── taskflow.db
└── README.md
---

# Environment Setup

## Requirements

- Python 3.10+
- pip
- Node.js and npm
- A modern web browser

## Backend Setup

From the project root:

```bash
python -m venv venv
---

# Running the Application

## Start the Backend

From the project root:

```bash
uvicorn backend.main:app --reload --port 8000
```
## Start the Frontend

Open a new terminal and go to the frontend directory:

```bash
cd frontend
npm install
npm run dev
```
## Algorithm Verification

To verify the correctness of the implemented algorithms, run:

```bash
python check_algorithms.py
```
The verification checks the implemented searching and sorting algorithms, including insertion sort, binary search, and linear search.
## Algorithm Benchmarking

To run the algorithm benchmarks, use:

```bash
python backend/benchmark.py
```

## Project Features

- Task creation and management
- Task status tracking
- Searching and sorting functionality
- Algorithm-based task processing
- Backend API using FastAPI
- Frontend interface using React
- Algorithm verification and benchmarking
## Technology Stack

### Backend
- Python
- FastAPI
- Uvicorn
- SQLite

### Frontend
- React
- Vite
- JavaScript
- CSS

### Algorithms
- Insertion Sort
- Binary Search
- Linear Search

## Project Workflow

1. The user interacts with the React frontend.
2. The frontend communicates with the FastAPI backend.
3. The backend processes task-related requests.
4. Tasks are stored and managed using SQLite.
5. Searching and sorting algorithms process task data where required.
6. Algorithm verification and benchmarking scripts are used to test performance and correctness.

## Testing

The project includes automated checks for the implemented algorithms.

To run the algorithm verification:

```bash
python check_algorithms.py
```
## Future Improvements

- Add user authentication and authorization
- Add task filtering and advanced search options
- Improve the frontend user experience
- Add more algorithm implementations
- Add automated testing for API endpoints
- Deploy the application for public access

## License

This project is developed as part of an academic capstone project.