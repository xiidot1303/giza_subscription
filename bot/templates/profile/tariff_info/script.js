
const button = document.getElementById("cancelSubscriptionButton");

button.onclick = function () {
    Telegram.WebApp.showConfirm(
      "Siz obunani bekor qilmoqchimisiz?",
      cancelSubscription
    );
};

async function cancelSubscription(have_to_cancel) {
    const apiHost = "{{ api_host }}";
    const subscriptionId = "{{ subscription.id }}";
    const userId = "{{ bot_user_id }}";
    if (have_to_cancel == true) {
        // send API to cancel subscription
        response = await fetch(`${apiHost}subscription/cancel`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                subscription_id: subscriptionId,
                bot_user_id: userId
            }),
        });
        const data = await response.json();
        if (data.success == true) {
            Telegram.WebApp.close();
        };

    }
};
