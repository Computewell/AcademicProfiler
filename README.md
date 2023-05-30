# High School API

![Repo size](https://img.shields.io/github/repo-size/Computewell/AcademicProfiler?style=round-square)
![Pep8 style](https://img.shields.io/badge/PEP8-style%20guide-purple?style=round-square)
![Latest commit](https://img.shields.io/github/last-commit/Computewell/AcademicProfiler/master?style=round-square)
![Contributors](https://img.shields.io/github/contributors/Computewell/AcademicProfiler?style=round-square)


The High School API is a RESTful API designed to manage various aspects of a high school, including administrators, teachers, students, parents, news articles, and more. It provides endpoints for performing CRUD operations on different resources and implements authentication and authorization using JWT (JSON Web Tokens).

It serves as a central interface for accessing and managing various aspects of the school's operations, including student information, course management, communication, resource access, event management, and reporting.

Through this API, users can authenticate and authorize access to the portal, ensuring secure interactions. Once authenticated, users can retrieve and update student-related data such as personal information, class schedules, attendance records, grades, and transcripts. They can also manage courses by retrieving information on courses, enrollments, teacher assignments, and assignment deadlines.

Communication features include sending messages, accessing notifications, and retrieving announcements, facilitating efficient and effective communication within the school community. Additionally, the API provides access to educational resources like documents, lecture notes, multimedia content, and assignments, supporting seamless resource sharing and collaboration.

The event management functionality allows users to retrieve school events, calendars, important dates, and extracurricular activities, ensuring everyone stays informed about upcoming events. Furthermore, the API enables the generation of reports on student performance, attendance, and other relevant metrics, providing valuable insights for educators and administrators.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Administrators**: Manage administrators' accounts and permissions.
- **Authentication and Authorization**: Implement secure authentication and authorization using JWT.
- **Teachers**: Manage teacher accounts, classes, and subjects.
- **Students**: Manage student accounts, classes, and grades.
- **Parents**: Access information about their child's progress and communicate with teachers.
- **News Articles**: Create, update, and delete news articles.
- **API Documentation**: Comprehensive documentation of all API endpoints and models.

## Getting Started

### Prerequisites

- Python 3.9 or above
- pip package manager
- PostgreSQL database

### Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/Computewell/AcademicProfiler.git
   ```
   
