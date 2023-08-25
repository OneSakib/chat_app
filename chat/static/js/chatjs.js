$(document).ready(() => {
  let $first_user = $("#first_user");
  // Show a specific div
  $first_user.removeClass("d-none");
  // Scroll to last Chat
  console.log("CALLED", $first_user);
  $first_user.animate(
    {
      scrollTop: $first_user.scrollHeight,
    },
    "slow"
  );
});
function chat_change(user_id) {
  // Hide all div first
  $(".chat-box").addClass("d-none");
  // Show a specific div
  $(`div[data-user-id=user_id_${user_id}]`).removeClass("d-none");
  // Scroll to last Chat
  $(`div[data-user-id=user_id_${user_id}]`).animate(
    {
      scrollTop: $(`div[data-user-id=user_id_${user_id}]`)[0].scrollHeight,
    },
    "slow"
  );
}
