import data from "@/data/booksignal.json";
import { Dashboard } from "@/components/dashboard";
import { parseDashboardData } from "@/data/contract";

export default function Home() {
  return <Dashboard data={parseDashboardData(data)} />;
}
