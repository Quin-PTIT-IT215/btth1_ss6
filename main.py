from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(
    title= 'QUẢN LÝ KHÓA HỌC',
    version= '1.0.0'
)

class CourseSchema(BaseModel):
    code: str
    name: str
    duration: int
    fee: float

courses = [
    {"id": 1, "code": "PY101", "name": "Python Basic", "duration": 30, "fee": 3000000},
    {"id": 2, "code": "API101", "name": "FastAPI Basic", "duration": 24, "fee": 2500000},
    {"id": 3, "code": "JV101", "name": "Java Basic", "duration": 40, "fee": 4000000}
]

@app.post('/courses', tags=['Courses'], status_code= status.HTTP_201_CREATED)
def add_course(course: CourseSchema):
    course_id = len(courses) + 1
    new_course = {
        'id': course_id,
        'code': course.code,
        'name': course.name,
        'duration': course.duration,
        'fee': course.fee
    }

    courses.append(new_course)
    return {
        'status_code': 201,
        'message': 'Thêm khóa học thành công',
        'data': courses
    }


@app.get('/courses', tags=['Scourses'], summary= 'Lấy danh sách khóa học')
def get_all_courses():
    return {
        'status_code': 200,
        'message': 'Lấy khóa học thành công',
        'data': courses
    }


@app.get('/courses/{course_id}', tags= ['Courses'], summary= 'Lấy chi tiết khóa học')
def get_detail_course(course_id: int):
    for course in courses:
        if course.get('id') == course_id:
            return {
                'status_code': 200,
                'message': 'Lấy khóa học thành công',
                'data': course
            }
    
    raise HTTPException(
        status_code = 404,
        detail = 'Không tìm thấy khóa học'
    )


@app.put("/courses/{course_id}", tags=['Courses'], summary= 'Cập nhật khóa học', status_code= 202)
def update_courses(course_id: int, update_course : CourseSchema):
    for course in courses:
        if course.get('id') == course_id:
            course['code'] = update_course.code
            course['name'] = update_course.name
            course['duration'] = update_course.duration
            course['fee'] = update_course.fee

            return {
                'status_code': 202,
                'message': 'Cập nhật khóa học thành công',
                'data': course
            }
    
    raise HTTPException(
        status_code= 404,
        detail= 'Không tìm thấy khóa học'
    )

@app.delete('/courses/{course_id}', tags=['Courses'], summary= 'Xóa khóa học')
def delete_course(course_id: int):
    for course in courses:
        if course_id == course.get('id'):
            courses.remove(course)
            return {
                'status_code': 200,
                'message': 'Xóa khóa học thành công',
                'data': course
            }
    
    raise HTTPException(
        status_code= 404,
        detail= 'Không tìm thấy khóa học'
    )