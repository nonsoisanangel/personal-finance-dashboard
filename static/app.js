document.addEventListener("DOMContentLoaded", () => {
    const modal = document.querySelector("#transactionModal");
    const openButton = document.querySelector("[data-open-modal]");
    const closeButton = document.querySelector("[data-close-modal]");

    if (modal && openButton && closeButton) {
        openButton.addEventListener("click", () => modal.showModal());
        closeButton.addEventListener("click", () => modal.close());
        modal.addEventListener("click", (event) => {
            if (event.target === modal) modal.close();
        });
    }

    const chartElement = document.querySelector("#expenseChart");
    const chartDataElement = document.querySelector("#chart-data");

    if (chartElement && chartDataElement && window.Chart) {
        const chartData = JSON.parse(chartDataElement.textContent);
        new Chart(chartElement, {
            type: "doughnut",
            data: {
                labels: chartData.labels,
                datasets: [{
                    data: chartData.values,
                    backgroundColor: ["#116149", "#d49c2f", "#d86c5a", "#477a96", "#765a91", "#5d8d73", "#be7d3c", "#8b9a93"],
                    borderWidth: 0,
                    hoverOffset: 5,
                }],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: "65%",
                plugins: {
                    legend: {
                        position: "bottom",
                        labels: { usePointStyle: true, padding: 18, font: { family: "DM Sans" } },
                    },
                },
            },
        });
    }
});
