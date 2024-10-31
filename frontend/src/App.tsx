import FileUpload from "./components/FileUpload";

const App = (): JSX.Element => {
  return (
    <div className="w-screen min-h-screen px-32 pt-10">
      <div className="flex flex-col gap-10 items-center">
        <h1 className="text-5xl font-extrabold">Rhombus AI Assessment</h1>
        <FileUpload />
      </div>
    </div>
  );
};

export default App;
