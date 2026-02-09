import React from 'react';

export const ResultTable = ({ users, onViewResults, onGeneratePDF, onResetTest, onViewAnswers }) => {
  const formatDate = (dateString) => {
    if (!dateString) return '-';
    try {
      return new Date(dateString).toLocaleDateString('ru-RU');
    } catch {
      return dateString;
    }
  };

  return (
    <div style={{ overflowX: 'auto' }}>
      <table className="table">
        <thead>
          <tr>
            <th>№</th>
            <th>Логин</th>
            <th>Статус</th>
            <th>Дата создания</th>
            <th>Дата завершения</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user, index) => (
            <tr key={user.id}>
              <td>{index + 1}</td>
              <td>{user.login}</td>
              <td>
                <span className={`badge ${user.isCompleted ? 'badge-success' : 'badge-warning'}`}>
                  {user.isCompleted ? 'Завершен' : 'В процессе'}
                </span>
              </td>
              <td>{formatDate(user.createdAt)}</td>
              <td>{formatDate(user.completedAt)}</td>
              <td>
                {user.isCompleted ? (
                  <div style={{ display: 'flex', gap: '5px', flexWrap: 'wrap' }}>
                    <button 
                      onClick={() => onViewResults(user)}
                      className="btn btn-sm btn-primary"
                      title="Просмотр результатов"
                    >
                      📊 Результаты
                    </button>
                    <button 
                      onClick={() => onGeneratePDF(user)}
                      className="btn btn-sm btn-success"
                      title="Скачать PDF отчет"
                    >
                      📄 PDF
                    </button>
                    <button 
                      onClick={() => onViewAnswers(user)}
                      className="btn btn-sm btn-info"
                      title="Просмотреть ответы"
                    >
                      📝 Ответы
                    </button>
                    <button 
                      onClick={() => onResetTest(user.id)}
                      className="btn btn-sm btn-warning"
                      title="Сбросить тест"
                    >
                      🔄 Сброс
                    </button>
                  </div>
                ) : (
                  <span style={{ color: '#999', fontSize: '12px' }}>Ожидает тестирования</span>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};