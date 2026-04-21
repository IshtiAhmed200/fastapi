import { useState, useEffect, useCallback } from 'react';
import { userService } from '../services/api';
import toast from 'react-hot-toast';
import {
  Modal,
  UserForm,
  UserTable,
  Pagination,
  LoadingSpinner,
  LoadingOverlay,
  EmptyState,
  ConfirmDialog,
} from '../components';
import { useAuth } from '../context/useAuth';

export default function UserListPage() {
  const [users, setUsers] = useState([]);
  const [totalPages, setTotalPages] = useState(1);
  const [currentPage, setCurrentPage] = useState(1);
  const [search, setSearch] = useState('');
  const [total, setTotal] = useState(0);
  const limit = 10;
  const { logout } = useAuth();

  const [isLoading, setIsLoading] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);

  const [selectedUser, setSelectedUser] = useState(null);

  const fetchUsers = useCallback(async (page, searchQuery) => {
    setIsLoading(true);
    try {
      const data = await userService.getUsers({
        page,
        limit,
        search: searchQuery,
      });
      setUsers(data.items || []);
      setTotalPages(data.total_pages || 1);
      setTotal(data.total || 0);
    } catch (error) {
      if (error.message.includes('401') || error.message.includes('Unauthorized')) {
        logout();
      }
      toast.error(error.message || 'Failed to fetch users');
    } finally {
      setIsLoading(false);
    }
  }, [limit, logout]);

  useEffect(() => {
    const timer = setTimeout(() => {
      fetchUsers(currentPage, search);
    }, 300);
    return () => clearTimeout(timer);
  }, [currentPage, search, fetchUsers]);

  const handleCreate = async (formData) => {
    setIsSubmitting(true);
    try {
      const userData = {
        email: formData.email,
        first_name: formData.first_name,
        last_name: formData.last_name,
        password: formData.password,
      };
      await userService.createUser(userData);
      toast.success('User created successfully');
      setIsCreateModalOpen(false);
      fetchUsers();
    } catch (error) {
      toast.error(error.message || 'Failed to create user');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleEdit = (user) => {
    setSelectedUser(user);
    setIsEditModalOpen(true);
  };

  const handleUpdate = async (formData) => {
    setIsSubmitting(true);
    try {
      const updateData = {
        first_name: formData.first_name,
        last_name: formData.last_name,
      };
      if (formData.password) {
        updateData.password = formData.password;
      }
      await userService.updateUser(selectedUser.id, updateData);
      toast.success('User updated successfully');
      setIsEditModalOpen(false);
      setSelectedUser(null);
      fetchUsers();
    } catch (error) {
      toast.error(error.message || 'Failed to update user');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDelete = (user) => {
    setSelectedUser(user);
    setIsDeleteDialogOpen(true);
  };

  const confirmDelete = async () => {
    setIsSubmitting(true);
    try {
      await userService.deleteUser(selectedUser.id);
      toast.success('User deleted successfully');
      setIsDeleteDialogOpen(false);
      setSelectedUser(null);
      fetchUsers();
    } catch (error) {
      toast.error(error.message || 'Failed to delete user');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handlePageChange = (page) => {
    setCurrentPage(page);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-6">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <h1 className="text-2xl font-bold text-gray-800">Users</h1>
              <p className="text-gray-500 mt-1">
                Manage your application users ({total} total)
              </p>
            </div>
            <button
              onClick={() => setIsCreateModalOpen(true)}
              className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
              </svg>
              Add User
            </button>
          </div>
        </div>

        <div className="mb-4">
          <div className="relative max-w-md">
            <input
              type="text"
              placeholder="Search users by name or email..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-10 pr-10 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <svg
              className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
            {search && (
              <button
                type="button"
                onClick={() => setSearch('')}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            )}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow overflow-hidden">
          {isLoading ? (
            <div className="p-12">
              <LoadingSpinner size="lg" />
            </div>
          ) : users.length === 0 ? (
            <EmptyState message="No users found. Create your first user!" />
          ) : (
            <UserTable
              users={users}
              onEdit={handleEdit}
              onDelete={handleDelete}
            />
          )}
          {totalPages > 1 && (
            <Pagination
              currentPage={currentPage}
              totalPages={totalPages}
              onPageChange={handlePageChange}
            />
          )}
        </div>
      </div>

      <Modal
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
        title="Create User"
      >
        <UserForm onSubmit={handleCreate} isLoading={isSubmitting} />
      </Modal>

      <Modal
        isOpen={isEditModalOpen}
        onClose={() => {
          setIsEditModalOpen(false);
          setSelectedUser(null);
        }}
        title="Edit User"
      >
        <UserForm
          onSubmit={handleUpdate}
          initialData={selectedUser}
          isEdit={true}
          isLoading={isSubmitting}
        />
      </Modal>

      <ConfirmDialog
        isOpen={isDeleteDialogOpen}
        onClose={() => {
          setIsDeleteDialogOpen(false);
          setSelectedUser(null);
        }}
        onConfirm={confirmDelete}
        isLoading={isSubmitting}
      />

      {isSubmitting && <LoadingOverlay />}
    </div>
  );
}