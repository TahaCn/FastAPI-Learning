from fastapi import FastAPI, Body, Path, Query, HTTPException
from typing import Optional
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

class Course:
    id:int
    title:str
    instructor:str
    rating:int
    published_date:int

    def __init__(self, id:int, title:str, instructor:str, rating:int, published_date:int):
        self.id = id
        self.title = title
        self.instructor = instructor
        self.rating = rating
        self.published_date = published_date

course = [
    Course(1,"Python", "Taha", 5, 2019),
    Course(2,"C++", "Micheal", 3, 2017),
    Course(3,"C#", "Jack", 2, 2020),
    Course(4,"Java", "Taha", 5, 2012),
    Course(5,"JavaScript", "Ahmet", 4, 2021),
    Course(6,"JavaScript", "Arda", 3, 2022),
]

class CourseRequest(BaseModel):
    id: Optional[int] = Field(description="The id of the course is optional", default= None)
    title:str = Field(min_length=3, max_length=100)
    instructor:str = Field(min_length=3)
    rating:int = Field(gt=0, lt=6)
    published_date:int = Field(gt=2000, lt=2100)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Python Taha",
                "instructor": "<NAME>",
                "rating": 5,
                "published_date": 2000
            }
        }
    }
@app.get("/courses", status_code=status.HTTP_200_OK)
async def get_courses():
    return course

@app.get("/courses/{course_id}", status_code=status.HTTP_200_OK)
async def get_course(course_id:int = Path(gt=0)):
    for c in course:
        if c.id == course_id:
            return c
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

@app.get("/courses/", status_code=status.HTTP_200_OK)
async def get_courses_by_rating(course_rating: int = Query(gt=0, lt=6)):
    course2 = []
    for c in course:
        if c.rating == course_rating:
            course2.append(c)
    return course2

@app.get("/courses/publish/", status_code=status.HTTP_200_OK)
async def get_courses_by_published_date(published_date:int = Query(gt=2000, lt=2050)):
    course2 = []
    for c in course:
        if c.published_date == published_date:
            course2.append(c)
    return course2

@app.post("/create-course", status_code=status.HTTP_201_CREATED)
async def create_course(c:CourseRequest):
    new_course = Course(**c.model_dump())
    course.append(find_course(new_course))


def find_course(c:Course):
    c.id = 1 if len(course) == 0 else course[-1].id + 1
    return c

@app.put("/courses/update-course", status_code=status.HTTP_204_NO_CONTENT)
async def update_course(c:CourseRequest):
    course_updated = False
    for i in range(len(course)):
        if course[i].id == c.id:
            course[i] = c
            course_updated = True
        if not course_updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")



@app.delete("/courses/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id:int = Path(gt=0)):
    course_deleted = False
    for i in range(len(course)):
        if course[i].id == course_id:
            course_deleted = True
            course.pop(i)
            break
        if not course_deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")