import React, { useState } from 'react';
import Button from './Button';

interface TaskFormProps {
  onSubmit: (title: string, description: string) => void;
  onCancel?: () => void;
  initialTitle?: string;
  initialDescription?: string;
  submitButtonText?: string;
}

const TaskForm: React.FC<TaskFormProps> = ({
  onSubmit,
  onCancel,
  initialTitle = '',
  initialDescription = '',
  submitButtonText = 'Add Task',
}) => {
  const [title, setTitle] = useState(initialTitle);
  const [description, setDescription] = useState(initialDescription);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) {
      alert('Task title cannot be empty');
      return;
    }
    onSubmit(title.trim(), description.trim());
    if (!initialTitle) { // Only clear fields if it's not an edit form
      setTitle('');
      setDescription('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mb-6 p-6 bg-white rounded-xl shadow-md border border-gray-200 max-w-2xl mx-auto">
      <div className="mb-5">
        <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">
          Title *
        </label>
        <input
          type="text"
          id="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200 text-base"
          placeholder="Enter task title"
          required
        />
      </div>
      <div className="mb-5">
        <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
          Description
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200 text-base"
          placeholder="Enter task description (optional)"
          rows={3}
        />
      </div>
      <div className="flex flex-col sm:flex-row sm:space-x-3 space-y-3 sm:space-y-0">
        <Button type="submit" variant="primary">
          {submitButtonText}
        </Button>
        {onCancel && (
          <Button type="button" onClick={onCancel} variant="secondary">
            Cancel
          </Button>
        )}
      </div>
    </form>
  );
};

export default TaskForm;