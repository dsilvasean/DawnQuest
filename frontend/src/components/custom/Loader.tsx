import { ClipLoader } from "react-spinners";

interface LoaderProps {
  loading: boolean;
  fullScreen?: boolean;
  size?: number;
  color?: string;
}

const Loader = ({ loading, fullScreen = false, size = 35, color = "#2563eb" }: LoaderProps) => {
  if (!loading) return null;

  if (fullScreen) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-white/60">
        <ClipLoader loading={loading} size={size} color={color} />
      </div>
    );
  }

  return <ClipLoader loading={loading} size={size} color={color} />;
};

export default Loader;
