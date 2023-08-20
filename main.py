from fastapi import FastAPI, HTTPException, status
from typing import Union, Optional
from pydantic import BaseModel


app = FastAPI()

class Course(BaseModel):
    title: str
    teacher: str
    students: Optional[list[str]] = []
    year: str


courses = {
    1: {
        "title": "Mathematics", 
        "teacher": "Daniel",
        "students": ["Tayo", "Ola", "Kazeem", "Dikajah"],
        "year": "basic"
    },

    2: {
        "title": "Statistics", 
        "teacher": "Quzeem",
        "students": ["Tayo", "Shade", "Femi", "Damilare"],
        "year": "advanced"
    },

    3: {
        "title": "Computer Science", 
        "teacher": "Munsor",
        "students": ["Tayo", "Ola", "Timothy", "Abdulquadri"],
        "year": "intermediate"
    }

}



@app.get("/api/courses")
def get_course(year: Union[str, None] = None):
    if year:
        year_course = []
        for index in courses.keys():
            if courses[index]["year"] == year:
                year_course.append(courses[index])
        year_course
    return courses 

@app.get("/api/courses/{course_id}/")
def get_course(course_id: int):
    try:
        return courses[course_id]
    except KeyError:
        raise HTTPException(
            status_code=404, detail=f'Course with id:{course_id} was not found'
        )


@app.delete("/api/courses/{course_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int):
    try:
        del courses[course_id]
    except KeyError:
        raise HTTPException(
            status_code=404, detail=f'Course with id:{course_id} was not found'
        )

@app.post("/api/courses/", status_code=status.HTTP_201_CREATED)
def create_course(new_course: Course):
    course_id = max(courses.keys()) + 1
    courses[course_id] = new_course.model_dump()
    return courses[course_id]

@app.put("/api/courses/{course_id}/")
def update_course(course_id: int, updated_course: Course):
    try:
        course = courses[course_id]
        course["title"] = updated_course.title
        course["teacher"] = updated_course.teacher
        course["students"] = updated_course.students
        course["year"] = updated_course.year
        return course
    except KeyError:
        raise HTTPException(
            status_code=404, detail=f'Course with id:{course_id} was not found'
        )


