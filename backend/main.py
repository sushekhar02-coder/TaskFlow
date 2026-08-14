
import time

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.database import Base, engine, get_db
from backend.models import User, Project, Task
from backend.schemas import (
    UserCreate,
    UserResponse,
    ProjectCreate,
    ProjectResponse,
    TaskCreate,
    TaskUpdate,
    TaskResponse,
)

from backend.algorithms import (
    insertion_sort,
    binary_search,
    linear_search,
)

from backend.quick_add import (
    build_prompt,
    parse_task_description,
    convert_due_date_hint,
)


# =========================================================
# DATABASE
# =========================================================

Base.metadata.create_all(bind=engine)


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(title="TaskFlow API")


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "DELETE",
    ],
    allow_headers=[
        "Content-Type",
        "Authorization",
    ],
)


# =========================================================
# REQUEST LOGGER
# =========================================================

@app.middleware("http")
async def request_logger(request, call_next):
    start_time = time.perf_counter()

    response = await call_next(request)

    elapsed = (time.perf_counter() - start_time) * 1000

    print(
        f"{request.method} {request.url.path} "
        f"- {elapsed:.2f} ms"
    )

    return response


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():
    return {
        "message": "TaskFlow API is running"
    }


# =========================================================
# USERS
# =========================================================

@app.post(
    "/users",
    response_model=UserResponse,
    status_code=201
)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=422,
            detail="Email already exists"
        )

    user = User(
        name=user_data.name,
        email=user_data.email
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@app.get(
    "/users",
    response_model=list[UserResponse]
)
def list_users(
    db: Session = Depends(get_db)
):
    return db.query(User).all()


# =========================================================
# PROJECTS
# =========================================================

@app.post(
    "/projects",
    response_model=ProjectResponse,
    status_code=201
)
def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db)
):
    owner = (
        db.query(User)
        .filter(User.id == project_data.owner_id)
        .first()
    )

    if not owner:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    project = Project(
        name=project_data.name,
        owner_id=project_data.owner_id
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


@app.get(
    "/projects",
    response_model=list[ProjectResponse]
)
def list_projects(
    db: Session = Depends(get_db)
):
    return db.query(Project).all()


# =========================================================
# CREATE TASK
# =========================================================

@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=201
)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db)
):
    project = (
        db.query(Project)
        .filter(Project.id == task_data.project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    task = Task(
        title=task_data.title,
        priority=task_data.priority,
        due_date=task_data.due_date,
        project_id=task_data.project_id,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


# =========================================================
# LIST TASKS
# =========================================================

@app.get(
    "/tasks",
    response_model=list[TaskResponse]
)
def list_tasks(
    sort: str | None = Query(default=None),
    db: Session = Depends(get_db)
):
    tasks = db.query(Task).all()

    records = [
        {
            "id": task.id,
            "title": task.title,
            "priority": task.priority,
            "due_date": task.due_date,
            "project_id": task.project_id,
        }
        for task in tasks
    ]

    # -------------------------
    # Sort by priority
    # -------------------------

    if sort == "priority":
        priority_rank = {
            "low": 1,
            "medium": 2,
            "high": 3,
        }

        for record in records:
            record["priority_rank"] = priority_rank[
                record["priority"]
            ]

        insertion_sort(records, "priority_rank")

        for record in records:
            del record["priority_rank"]

        return records

    return tasks


# =========================================================
# SEARCH TASKS
# =========================================================

@app.get(
    "/tasks/search",
    response_model=TaskResponse
)
def search_tasks(
    title: str,
    algo: str = "binary",
    db: Session = Depends(get_db)
):
    tasks = db.query(Task).all()

    records = [
        {
            "id": task.id,
            "title": task.title,
        }
        for task in tasks
    ]

    # -------------------------
    # Binary search
    # -------------------------

    if algo == "binary":
        insertion_sort(records, "title")

        index = binary_search(
            records,
            title,
            "title"
        )

    # -------------------------
    # Linear search
    # -------------------------

    elif algo == "linear":
        index = linear_search(
            records,
            title,
            "title"
        )

    else:
        raise HTTPException(
            status_code=422,
            detail="algo must be binary or linear"
        )

    # -------------------------
    # Task not found
    # -------------------------

    if index == -1:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task_id = records[index]["id"]

    task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

    return task


# =========================================================
# GET SINGLE TASK
# =========================================================

@app.get(
    "/tasks/{task_id}",
    response_model=TaskResponse
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


# =========================================================
# UPDATE TASK
# =========================================================

@app.put(
    "/tasks/{task_id}",
    response_model=TaskResponse
)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db)
):
    task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if task_data.title is not None:
        task.title = task_data.title

    if task_data.priority is not None:
        task.priority = task_data.priority

    if task_data.due_date is not None:
        task.due_date = task_data.due_date

    db.commit()
    db.refresh(task)

    return task


# =========================================================
# DELETE TASK
# =========================================================

@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return {
        "message": "Task deleted successfully"
    }


# =========================================================
# PROJECT STATISTICS
# =========================================================

@app.get("/projects/statistics")
def project_statistics(
    db: Session = Depends(get_db)
):
    results = (
        db.query(
            Project.id.label("project_id"),
            Project.name.label("project_name"),
            func.count(Task.id).label("task_count"),
            Task.status.label("status"),
            func.count(Task.status).label("status_count"),
        )
        .outerjoin(
            Task,
            Project.id == Task.project_id
        )
        .group_by(
            Project.id,
            Project.name,
            Task.status
        )
        .all()
    )

    statistics = {}

    for row in results:
        project_id = row.project_id

        if project_id not in statistics:
            statistics[project_id] = {
                "project_id": project_id,
                "project_name": row.project_name,
                "task_count": 0,
                "count_by_status": {}
            }

        if row.status is not None:
            statistics[project_id]["count_by_status"][
                row.status
            ] = row.status_count

    totals = (
        db.query(
            Project.id,
            func.count(Task.id)
        )
        .outerjoin(Task)
        .group_by(Project.id)
        .all()
    )

    for project_id, total in totals:
        if project_id in statistics:
            statistics[project_id]["task_count"] = total

    return list(statistics.values())


# =========================================================
# QUICK ADD TASK
# =========================================================

@app.post(
    "/tasks/quick-add",
    response_model=TaskResponse,
    status_code=201
)
def quick_add_task(
    data: dict,
    db: Session = Depends(get_db)
):
    # -------------------------
    # Read input
    # -------------------------

    description = data.get("description")
    project_id = data.get("project_id")

    # -------------------------
    # Validate description
    # -------------------------

    if not isinstance(description, str):
        raise HTTPException(
            status_code=422,
            detail="description is required and must be a string"
        )

    description = description.strip()

    if not description:
        raise HTTPException(
            status_code=422,
            detail="description cannot be empty"
        )

    # -------------------------
    # Validate project ID
    # -------------------------

    if not isinstance(project_id, int):
        raise HTTPException(
            status_code=422,
            detail="project_id is required and must be an integer"
        )

    # -------------------------
    # Check project
    # -------------------------

    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=422,
            detail="project_id does not reference an existing project"
        )

    # -------------------------
    # Parse task description
    # -------------------------

    prompt = build_prompt(description)

    parsed = parse_task_description(description)

    # -------------------------
    # Convert due date
    # -------------------------

    due_date = convert_due_date_hint(
        parsed["due_date_hint"]
    )

    # -------------------------
    # Create task data
    # -------------------------

    task_data = TaskCreate(
        title=parsed["title"],
        priority=parsed["priority"],
        due_date=due_date,
        project_id=project_id,
    )

    # -------------------------
    # Create database task
    # -------------------------

    task = Task(
        title=task_data.title,
        priority=task_data.priority,
        due_date=task_data.due_date,
        project_id=task_data.project_id,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task