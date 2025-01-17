import { headers } from "next/headers";
import { redirect } from "next/navigation";

const HealthPage = async () => {
    const headersList = await headers();
    const userAgent = headersList.get("User-Agent") || headersList.get("user-agent") || "";

    if (userAgent !== "service-status") {
        redirect("/");
    }

    return <div>OK</div>;
};

export default HealthPage;
