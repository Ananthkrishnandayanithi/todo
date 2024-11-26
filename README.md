# Django Task Manager Application

## Overview

This project is a Django-based Task Manager application that allows users to:
- Register and log in.
- Create, view, update, and delete tasks.
- Search for tasks and filter based on completion.

---

## **Functionality**

Below is an explanation of each class and function in the project:

### **Authentication Views**

#### 1. **`CustomLoginView`**
- Extends: `LoginView`
- Purpose: Handles user login functionality.
- Key Features:
  - Uses the `base/login.html` template.
  - Redirects authenticated users to the task list page.
  - Overrides the `get_success_url` method to redirect users to `task-list` upon successful login.
  - ![image](https://github.com/user-attachments/assets/c1b52ce5-cbd2-4de5-a6ff-eebeeb841936)


#### 2. **`RegisterPage`**
- Extends: `FormView`
- Purpose: Handles user registration using Django's built-in `UserCreationForm`.
- Key Features:
  - Uses the `base/register.html` template.
  - Automatically logs in the user after successful registration.
  - Redirects authenticated users to the task list if they try to access the registration page.
  ![image](https://github.com/user-attachments/assets/40ffad0a-0779-407a-a612-312905cb32cb)



#### 3. **`TaskList`**
- Extends: `ListView`
- Purpose: Displays all tasks for the currently logged-in user.
- Key Features:
  - Filters tasks to show only those belonging to the authenticated user.
  - Provides a task count for incomplete tasks (`complex=False`).
  - Supports search functionality (`title__icontains=search-input`).
    ![image](https://github.com/user-attachments/assets/78076107-d144-4d29-a88f-cced995ecec6)


#### 4. **`TaskDetail`**
- Extends: `DetailView`
- Purpose: Displays detailed information about a specific task.
- Key Features:
  - Uses the `base/task.html` template.
  - Ensures only the logged-in user can view their tasks.
    ![image](https://github.com/user-attachments/assets/83ffc8a6-4935-406a-a329-a69f459f3db9)


#### 5. **`TaskCreate`**
- Extends: `CreateView`
- Purpose: Allows users to create a new task.
- Key Features:
  - Uses the `base/task_form.html` template (Django default for `CreateView`).
  - Fields: `title`, `description`, `complete`, `complex`.
  - Automatically associates the task with the currently logged-in user.
    ![image](https://github.com/user-attachments/assets/3a468be6-6c41-49f5-b0d0-b2a85475c624)


#### 6. **`TaskUpdate`**
- Extends: `UpdateView`
- Purpose: Allows users to update an existing task.
- Key Features:
  - Uses the `base/task_form.html` template.
  - Fields: `title`, `description`, `complete`, `complex`.
    ![image](https://github.com/user-attachments/assets/8f7246ca-75ca-4dd4-9acd-e36e5fdc1328)


#### 7. **`TaskDelete`**
- Extends: `DeleteView`
- Purpose: Allows users to delete a task.
- Key Features:
  - Uses the `base/task_confirm_delete.html` template.
  - Redirects to the task list page after successful deletion.
    
![image](https://github.com/user-attachments/assets/b7b7a24d-69a4-4510-b586-801e7cd1912b)


## **Templates**

### **Templates Used**
1. **`login.html`**:
   - Used for user login.
   - Includes a form for username and password input.
   
2. **`register.html`**:
   - Used for new user registration.
   - Provides fields for username, password, and password confirmation.

3. **`task_list.html`**:
   - Displays the list of tasks for the user.
   - Includes a search bar for filtering tasks.

4. **`task.html`**:
   - Shows detailed information for a specific task.

5. **`task_confirm_delete.html`**:
   - Asks the user to confirm before deleting a task.

