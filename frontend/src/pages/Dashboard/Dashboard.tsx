import './Dashboard.css';
import DashboardTop from './DashboardTop';
import DashboardBottom from './DashboardBottom';

function Dashboard() {
  return (
    <div className="dashboard-container">
      <div className="dashboard-top">
        <DashboardTop />
      </div>

      <div className="dashboard-bottom">
        <DashboardBottom />
      </div>
    </div>
  );
}

export default Dashboard;
