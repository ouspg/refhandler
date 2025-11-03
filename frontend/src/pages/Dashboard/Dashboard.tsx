import './Dashboard.css';
import LeftPanel from './LeftPanel';
import RightPanel from './RightPanel';

function Dashboard() {
  return (
    <div className="dashboard-container">
      <div className="dashboard-left-column">
        <LeftPanel />
      </div>

      <div className="dashboard-right-column">
        <RightPanel />
      </div>
    </div>
  );
}

export default Dashboard;
