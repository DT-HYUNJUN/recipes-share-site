const reviewSection = document.querySelector("#reviews");
const reviews = document.querySelectorAll("#review");

const reviewForm = document.querySelector("#review-form");
const reviewField = document.querySelector("#id_content");
reviewField.setAttribute("rows", "2");
reviewField.setAttribute("placeholder", "여기에 리뷰를 작성해보세요!");
reviewField.classList.add("border-0");
reviewField.classList.add("focus:ring-0");
reviewField.classList.add("resize-none");

const divIdContent = document.querySelector("#div_id_content");
const labelTag = divIdContent.querySelector("label");
labelTag.classList.add("hidden");

const reviewCount = document.querySelector("#review-count");

reviews.forEach((review) => {
  const dropdownBtn = review.querySelector("#dropdownDefaultButton");
  const pk = review.dataset.reviewPk;
  const dropdown = review.querySelector(`#dropdown-${pk}`);
  const commentTextarea = review.querySelector("#comment-textarea");
  const input = review.querySelector("#review-update-field");
  const aTags = review.querySelectorAll("a");
  const editBtn = review.querySelector("#edit-btn");
  const deleteBtn = review.querySelector("#delete-btn");
  const submitBtn = review.querySelector("#submit-btn");
  const cancelBtn = review.querySelector("#cancel-btn");
  const reviewContent = review.querySelector("#review-content");

  if (editBtn) {
    editBtn.addEventListener("click", () => {
      reviewContent.classList.add("hidden");
      commentTextarea.classList.remove("hidden");
      dropdown.classList.add("hidden");
      dropdownBtn.classList.add("hidden");
    });

    cancelBtn.addEventListener("click", () => {
      reviewContent.classList.remove("hidden");
      commentTextarea.classList.add("hidden");
      dropdownBtn.classList.remove("hidden");
    });

    submitBtn.addEventListener("click", () => {
      let param = {
        pk: review.dataset.reviewPk,
        content: input.value,
      };

      $.ajax({
        url: review.dataset.updateUrl,
        type: "POST",
        headers: {
          "X-CSRFTOKEN": review.dataset.csrftoken,
        },
        data: JSON.stringify(param),
        success: function (data) {
          reviewContent.textContent = data.content;
          commentTextarea.classList.add("hidden");
          reviewContent.classList.remove("hidden");
          dropdownBtn.classList.remove("hidden");
        },
        error: function () {
          alert("오류!");
        },
      });
    });

    deleteBtn.addEventListener("click", () => {
      let param = {
        review_pk: review.dataset.reviewPk,
        recipe_pk: review.dataset.recipePk,
      };

      $.ajax({
        url: review.dataset.deleteUrl,
        type: "POST",
        headers: {
          "X-CSRFTOKEN": review.dataset.csrftoken,
        },
        data: JSON.stringify(param),
        success: function (data) {
          reviewSection.removeChild(review);
          reviewCount.textContent = parseInt(reviewCount.textContent) - 1;
        },
        error: function () {
          alert("오류!");
        },
      });
    });
  }
});

// 리뷰
const reviewSubmit = reviewForm.querySelector("#review_create_submit");
reviewSubmit.addEventListener("click", (e) => {
  e.preventDefault();
  let param = {
    pk: reviewForm.dataset.pk,
    content: reviewField.value,
  };
  $.ajax({
    url: reviewForm.dataset.url,
    type: "POST",
    headers: {
      "X-CSRFTOKEN": reviewForm.dataset.csrftoken,
    },
    data: JSON.stringify(param),
    success: function (data) {
      console.log(data);
      const reviewElement = document.createElement("div"); // 새로운 댓글 요소 생성
      reviewElement.setAttribute("id", "review");
      reviewElement.setAttribute(
        "data-csrftoken",
        reviewForm.dataset.csrftoken
      );
      reviewElement.setAttribute("data-recipe-pk", reviewForm.dataset.pk);
      reviewElement.setAttribute("data-review-pk", data.review_pk); // 생성된 댓글의 PK 값
      reviewElement.setAttribute("data-update-url", "/recipes/review_update/");
      reviewElement.classList.add(
        "grid",
        "grid-cols-12",
        "text-sm",
        "gap-3",
        "py-5",
        "px-3",
        "border-b",
        "bg-[#9ACD32]/[0.2]",
        "dark:bg-green-900",
      );

      const profileImageWrapper = document.createElement("div");
      profileImageWrapper.classList.add(
        "col-span-1",
        "flex",
        "items-start",
        "mb-1"
      );

      // 리뷰 작성자 프로필 사진
      const profileImage = document.createElement("img");
      profileImage.setAttribute("class", "w-10 rounded-full");
      if (data.profile_image) {
        profileImage.setAttribute("src", data.profile_image);
      } else {
        profileImage.setAttribute(
          "src",
          "http://127.0.0.1:8000/static/img/profile_image2.png"
        );
      }
      profileImage.setAttribute("alt", "profile");
      profileImageWrapper.appendChild(profileImage);
      reviewElement.appendChild(profileImageWrapper);

      // 작성자 / 내용
      const contentContainer = document.createElement("div");
      contentContainer.classList.add("col-span-11");

      const authorContainer = document.createElement("div");
      authorContainer.classList.add("flex", "justify-between");

      const authorName = document.createElement("p");
      authorName.classList.add("font-bold", "mb-1", "dark:text-white");
      authorName.textContent = data.nickname;
      authorContainer.appendChild(authorName);

      // 드롭다운 버튼
      const newDropdownBtnWrapper = document.createElement("div");

      const newDropdownBtn = document.createElement("button");
      newDropdownBtn.setAttribute("id", "dropdownDefaultButton");
      newDropdownBtn.setAttribute(
        "data-dropdown-toggle",
        `dropdown-${data.review_pk}`
      );
      newDropdownBtn.setAttribute("type", "button");

      const newDropdownBtnIcon = document.createElement("i");
      newDropdownBtnIcon.classList.add("bi", "bi-three-dots-vertical");

      newDropdownBtn.appendChild(newDropdownBtnIcon);

      // 드롭다운 컨텐츠
      const newDropdownContentWrapper = document.createElement("div");
      newDropdownContentWrapper.setAttribute(
        "id",
        `dropdown-${data.review_pk}`
      );
      newDropdownContentWrapper.classList.add(
        "z-10",
        "hidden",
        "bg-white",
        "divide-y",
        "divide-gray-100",
        "rounded-lg",
        "shadow",
        "w-20",
        "dark:bg-gray-700"
      );
      newDropdownContentWrapper.setAttribute("data-popper-placement", "bottom");
      // newDropdownContentWrapper.setAttribute('style', 'position: absolute; inset: 0px auto auto 0px; margin: 0px; transform: translate3d(1693.33px, 3464px, 0px);')

      const newDropdownContentUl = document.createElement("ul");
      newDropdownContentUl.classList.add(
        "py-2",
        "text-sm",
        "text-gray-700",
        "dark:text-gray-200"
      );
      newDropdownContentUl.setAttribute(
        "aria-labelledby",
        "dropdownDefaultButton"
      );

      const newDropdownContentLiEdit = document.createElement("li");

      const newDropdownContentLiEditAtag = document.createElement("a");
      newDropdownContentLiEditAtag.setAttribute("id", "edit-btn");
      newDropdownContentLiEditAtag.classList.add(
        "block",
        "m-0",
        "px-4",
        "py-2",
        "hover:bg-gray-100",
        "dark:hover:bg-gray-600",
        "dark:hover:text-white",
        "cursor-pointer"
      );
      newDropdownContentLiEditAtag.textContent = "수정";

      const newDropdownContentLiDelete = document.createElement("li");

      const newDropdownContentLiDeleteAtag = document.createElement("a");
      newDropdownContentLiDeleteAtag.setAttribute("id", "delete-btn");
      newDropdownContentLiDeleteAtag.classList.add(
        "block",
        "m-0",
        "px-4",
        "py-2",
        "hover:bg-gray-100",
        "dark:hover:bg-gray-600",
        "dark:hover:text-white",
        "cursor-pointer"
      );
      newDropdownContentLiDeleteAtag.textContent = "삭제";

      newDropdownContentLiEdit.appendChild(newDropdownContentLiEditAtag);
      newDropdownContentLiDelete.appendChild(newDropdownContentLiDeleteAtag);

      newDropdownContentUl.appendChild(newDropdownContentLiEdit);
      newDropdownContentUl.appendChild(newDropdownContentLiDelete);

      newDropdownContentWrapper.appendChild(newDropdownContentUl);

      newDropdownBtnWrapper.appendChild(newDropdownBtn);
      newDropdownBtnWrapper.appendChild(newDropdownContentWrapper);

      authorContainer.appendChild(newDropdownBtnWrapper);

      contentContainer.appendChild(authorContainer);

      // newDropdownBtnWrapper.addEventListener('click', () => {
      //   newDropdownContentWrapper.classList.remove('hidden')
      //   newDropdownContentWrapper.classList.add('block')
      // })

      const reviewContent = document.createElement("p");
      reviewContent.setAttribute("id", "review-content");
      reviewContent.classList.add("col-span-6", "flex", "items-center", "mb-2", "dark:text-gray-300");
      reviewContent.textContent = data.content;
      contentContainer.appendChild(reviewContent);

      // 댓글 수정 부분 생략

      const timestamp = document.createElement("span");
      timestamp.classList.add("text-gray-500");
      timestamp.textContent = formatDate(data.created_at);
      contentContainer.appendChild(timestamp);

      reviewElement.appendChild(contentContainer);
      console.log(reviewElement);
      reviewSection.appendChild(reviewElement); // 생성된 댓글 요소 추가
      console.log(reviewSection);
      reviewCount.textContent = parseInt(reviewCount.textContent) + 1;
      reviewField.value = "";
    },
    error: function () {
      alert("오류!");
    },
  });
});

function formatDate(isoString) {
  const date = new Date(isoString);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  const hours = String(date.getHours()).padStart(2, "0");
  const minutes = String(date.getMinutes()).padStart(2, "0");

  const formattedDate = `${year}-${month}-${day} ${hours}:${minutes}`;
  return formattedDate;
}
