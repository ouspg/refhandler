import ItemManagement from '../../components/ItemManagement';

function ProjectManagement() {
  return (
    <div>
      <h1>Project management page</h1>
      <ItemManagement pageName="Project" onAdd={() => {console.log('add project clicked')}} />
    </div>
  );
}

export default ProjectManagement;
