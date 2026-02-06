'use client';

import React, { useState, useEffect } from 'react';
import TaskList from '../components/TaskList';
import TaskForm from '../components/TaskForm';
import ApiClient, { Task } from '../services/apiClient';

const HomePage: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [editingTask, setEditingTask] = useState<Task | null>(null);

  // Load tasks on component mount
  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    try {
      setLoading(true);
      const tasksData = await ApiClient.getAllTasks();
      setTasks(tasksData);
    } catch (error) {
      console.error('Error loading tasks:', error);
      alert('Failed to load tasks. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleAddTask = async (title: string, description: string) => {
    try {
      const newTask = await ApiClient.createTask({ title, description });
      setTasks([...tasks, newTask]);
    } catch (error) {
      console.error('Error adding task:', error);
      alert('Failed to add task. Please try again.');
    }
  };

  const handleUpdateTask = async (id: number, title: string, description: string) => {
    try {
      const updatedTask = await ApiClient.updateTask(id, { title, description });
      setTasks(tasks.map(task => task.id === id ? updatedTask : task));
      setEditingTask(null);
    } catch (error) {
      console.error('Error updating task:', error);
      alert('Failed to update task. Please try again.');
    }
  };

  const handleToggleTask = async (id: number) => {
    try {
      const toggledTask = await ApiClient.toggleTaskStatus(id);
      setTasks(tasks.map(task => task.id === id ? toggledTask : task));
    } catch (error) {
      console.error('Error toggling task status:', error);
      alert('Failed to update task status. Please try again.');
    }
  };

  const handleDeleteTask = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await ApiClient.deleteTask(id);
        setTasks(tasks.filter(task => task.id !== id));
      } catch (error) {
        console.error('Error deleting task:', error);
        alert('Failed to delete task. Please try again.');
      }
    }
  };

  const handleEditTask = (id: number) => {
    const task = tasks.find(t => t.id === id);
    if (task) {
      setEditingTask(task);
    }
  };

  const handleCancelEdit = () => {
    setEditingTask(null);
  };

  if (loading) {
    return (
      <div className="text-center py-16">
        <h1 className="text-3xl font-bold text-gray-800 mb-4">Loading Tasks...</h1>
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500"></div>
      </div>
    );
  }

  return (
    <div className="w-full">
      <div className="text-center mb-10">
        <h1 className="text-4xl font-bold text-gray-800 mb-3">Todo List</h1>
        <p className="text-gray-600">Organize your tasks efficiently</p>
      </div>

      {/* Add Task Form */}
      {!editingTask && (
        <div className="mb-10">
          <TaskForm onSubmit={handleAddTask} submitButtonText="Add Task" />
        </div>
      )}

      {/* Edit Task Form */}
      {editingTask && (
        <div className="mb-10">
          <TaskForm
            initialTitle={editingTask.title}
            initialDescription={editingTask.description || ''}
            onSubmit={(title, description) => handleUpdateTask(editingTask.id, title, description)}
            onCancel={handleCancelEdit}
            submitButtonText="Update Task"
          />
        </div>
      )}

      {/* Task List */}
      <TaskList
        tasks={tasks}
        onToggle={handleToggleTask}
        onDelete={handleDeleteTask}
        onEdit={handleEditTask}
      />
    </div>
  );
};

export default HomePage;