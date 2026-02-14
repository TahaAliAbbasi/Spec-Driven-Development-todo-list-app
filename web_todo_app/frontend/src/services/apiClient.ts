// Define the Task type to match the backend API response
export interface Task {
  id: number;
  title: string;
  description: string | null;
  is_completed: boolean;
  created_at: string; // ISO date string
  updated_at: string; // ISO date string
}

// Define the request types
export interface CreateTaskRequest {
  title: string;
  description?: string;
}

export interface UpdateTaskRequest {
  title?: string;
  description?: string;
  is_completed?: boolean;
}

// Base API URL - defaults to localhost:8000 for development
const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001/v1';

/**
 * API client service for task operations
 */
class ApiClient {
  /**
   * Fetch all tasks
   */
  static async getAllTasks(): Promise<Task[]> {
    try {
      const response = await fetch(`${BASE_URL}/tasks`);

      if (!response.ok) {
        throw new Error(`Failed to fetch tasks: ${response.status} ${response.statusText}`);
      }

      const tasks: Task[] = await response.json();
      return tasks;
    } catch (error) {
      console.error('Error fetching tasks:', error);
      throw error;
    }
  }

  /**
   * Create a new task
   */
  static async createTask(taskData: CreateTaskRequest): Promise<Task> {
    try {
      const response = await fetch(`${BASE_URL}/tasks`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: taskData.title,
          description: taskData.description || null,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Failed to create task: ${response.status} ${response.statusText}`);
      }

      const task: Task = await response.json();
      return task;
    } catch (error) {
      console.error('Error creating task:', error);
      throw error;
    }
  }

  /**
   * Get a specific task by ID
   */
  static async getTaskById(id: number): Promise<Task> {
    try {
      const response = await fetch(`${BASE_URL}/tasks/${id}`);

      if (!response.ok) {
        throw new Error(`Failed to fetch task: ${response.status} ${response.statusText}`);
      }

      const task: Task = await response.json();
      return task;
    } catch (error) {
      console.error(`Error fetching task ${id}:`, error);
      throw error;
    }
  }

  /**
   * Update a task
   */
  static async updateTask(id: number, taskData: UpdateTaskRequest): Promise<Task> {
    try {
      const response = await fetch(`${BASE_URL}/tasks/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(taskData),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Failed to update task: ${response.status} ${response.statusText}`);
      }

      const task: Task = await response.json();
      return task;
    } catch (error) {
      console.error(`Error updating task ${id}:`, error);
      throw error;
    }
  }

  /**
   * Toggle task completion status
   */
  static async toggleTaskStatus(id: number): Promise<Task> {
    try {
      const response = await fetch(`${BASE_URL}/tasks/${id}/toggle-status`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Failed to toggle task status: ${response.status} ${response.statusText}`);
      }

      const task: Task = await response.json();
      return task;
    } catch (error) {
      console.error(`Error toggling task ${id} status:`, error);
      throw error;
    }
  }

  /**
   * Delete a task
   */
  static async deleteTask(id: number): Promise<void> {
    try {
      const response = await fetch(`${BASE_URL}/tasks/${id}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Failed to delete task: ${response.status} ${response.statusText}`);
      }
    } catch (error) {
      console.error(`Error deleting task ${id}:`, error);
      throw error;
    }
  }
}

export default ApiClient;