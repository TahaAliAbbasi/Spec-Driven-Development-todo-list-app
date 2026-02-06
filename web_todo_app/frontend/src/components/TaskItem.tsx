import React from 'react';
import { Task } from '../types/task';
import Button from './Button';

interface TaskItemProps {
  task: Task;
  onToggle: (id: number) => void;
  onDelete: (id: number) => void;
  onEdit: (id: number) => void;
}

const TaskItem: React.FC<TaskItemProps> = ({ task, onToggle, onDelete, onEdit }) => {
  return (
    <div className={`flex flex-col sm:flex-row sm:items-center justify-between p-5 mb-4 bg-white rounded-xl shadow-sm border border-gray-200 transition-all duration-200 hover:shadow-md ${task.is_completed ? 'opacity-80' : ''}`}>
      <div className="flex items-start mb-3 sm:mb-0">
        <input
          type="checkbox"
          checked={task.is_completed}
          onChange={() => onToggle(task.id)}
          className="mt-1 mr-4 h-5 w-5 text-primary-600 rounded focus:ring-primary-500 focus:ring-2 min-h-5 min-w-5"
        />
        <div className="flex-1">
          <h3 className={`font-medium ${task.is_completed ? 'line-through text-gray-500' : 'text-gray-800'} text-lg`}>
            {task.title}
          </h3>
          {task.description && (
            <p className={`text-sm ${task.is_completed ? 'line-through text-gray-400' : 'text-gray-600'} mt-2`}>
              {task.description}
            </p>
          )}
          <p className="text-xs text-gray-400 mt-2">
            Created: {new Date(task.created_at).toLocaleDateString()}
          </p>
        </div>
      </div>
      <div className="flex space-x-2 sm:ml-4 flex-shrink-0">
        <Button onClick={() => onEdit(task.id)} variant="secondary" size="sm">
          Edit
        </Button>
        <Button onClick={() => onDelete(task.id)} variant="error" size="sm">
          Delete
        </Button>
      </div>
    </div>
  );
};

export default TaskItem;