const demo_dict = {};
var common_translations = {};

const CARD_TEMPLATE = `<div id="card_template" class="demo-card wp-block-group has-white-background-color has-background">
  <div class="card-body">
    <h4 class="has-text-align-center card-title">DEMO TITLE</h4>
    <div class="masteriyo-course--content__rt">
      <div class="masteriyo-course-author">
        <a href="">
          <img src="" alt="instructor image" srcset="">
          <span class="masteriyo-course-author--name">Instructor</span>
        </a>
      </div>
    </div>
    <p class="card-text">DEMO DESCRIPTION</p>
  </div>
  <div class="card-footer">
    <div class="card-status">
      <div class="card-time">
        <div class="has-tooltip">
          <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20px"
              height="20px"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
              class="mr-50 feather feather-clock"
              >
              <circle cx="12" cy="12" r="10"></circle>
              <polyline points="12 6 12 12 16 14"></polyline>
          </svg>
          <div class="tooltip">
            <span> Estimated time to complete the Demo </span>
          </div>
        </div>
        <span class=time-text> 20min </span>
      </div>
      <div class="card-difficulty">
        <div class="has-tooltip">
          <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20px"
              height="20px"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
              class="mr-50 feather feather-bar-chart"
              >
              <line x1="12" y1="20" x2="12" y2="10"></line>
              <line x1="18" y1="20" x2="18" y2="4"></line>
              <line x1="6" y1="20" x2="6" y2="16"></line>
          </svg>
          <div class="tooltip">
            <span> Estimated difficulty of the Demo </span>
          </div>
        </div>
        <span class=level-text> Intermediate </span>
      </div>
      <div class="card-hardware">
        <div class="has-tooltip">
        <svg class="mr-50 feather feather-clock" width="20px" height="20px" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" version="1.1" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <g transform="matrix(.021215 0 0 .021215 -.70427 -.7287)" fill="#7367f0" stroke="none">
            <path d="m852 177.6h-196.8c-22.801-32.398-56.398-55.199-94.801-64.801-6-39.602-40.801-70.801-82.801-70.801s-76.801 31.199-82.801 70.801c-38.398 9.6016-70.801 32.398-94.801 64.801h-195.6c-9.6016 0-18 8.3984-18 18v944.4c0 9.6016 8.3984 18 18 18h747.6c9.6016 0 18-8.3984 18-18v-944.4c0-10.801-8.3984-18-18-18zm-435.6-32.402c8.3984-1.1992 15.602-9.6016 15.602-18v-1.1992c0-26.398 21.602-48 48-48s48 21.602 48 48v2.3984c0 8.3984 6 16.801 15.602 18 37.199 6 69.602 27.602 90 60 9.6016 15.602 15.602 32.398 19.199 50.398l-345.6 4e-3c2.3984-18 8.3984-34.801 19.199-50.398 19.203-33.602 52.801-55.203 90-61.203zm417.6 976.8h-711.6v-908.4h158.4v1.1992c-3.6016 8.3984-6 18-7.1992 26.398 0 1.1992 0 2.3984-1.1992 3.6016 0 3.6016-1.1992 7.1992-1.1992 10.801v3.6016c0 4.8008-1.1992 9.6016-1.1992 14.398 0 9.6016 8.3984 18 18 18h380.4c9.6016 0 18-8.3984 18-18 0-4.8008 0-9.6016-1.1992-14.398v-3.6016c0-3.6016-1.1992-7.1992-1.1992-10.801 0-1.1992 0-2.3984-1.1992-3.6016-1.1992-4.8008-2.3984-9.6016-3.6016-13.199-1.1992-4.8008-2.3984-8.3984-4.8008-13.199v-1.1992h158.4l4e-3 908.4z"/>
            <path d="m1018.8 236.4c-51.602 0-94.801 42-94.801 94.801v591.6c0 1.1992 1.1992 2.3984 1.1992 2.3984v1.1992l76.801 132c3.6016 6 9.6016 8.3984 15.602 8.3984s12-3.6016 15.602-8.3984l76.801-132v-1.1992c0-1.1992 1.1992-2.3984 1.1992-2.3984v-591.6c2.4023-51.598-40.801-94.801-92.398-94.801zm-58.801 662.4v-514.8h117.6v513.6h-117.6zm58.801-626.4c32.398 0 58.801 26.398 58.801 58.801v16.801h-117.6v-16.801c0-32.398 26.398-58.801 58.801-58.801zm0 740.4-45.602-78h90z"/>
            <path d="m333.6 870h-117.6c-9.6016 0-18 8.3984-18 18v117.6c0 9.6016 8.3984 18 18 18h117.6c9.6016 0 18-8.3984 18-18v-117.6c0-9.6016-7.2031-18-18-18zm-18 117.6h-81.602v-81.602h81.602z"/>
            <path d="m390 466.8c0 9.6016 8.3984 18 18 18h333.6c9.6016 0 18-8.3984 18-18s-8.3984-18-18-18h-333.6c-9.6016 0-18 8.3984-18 18z"/>
            <path d="m741.6 688.8h-333.6c-9.6016 0-18 8.3984-18 18s8.3984 18 18 18h333.6c9.6016 0 18-8.3984 18-18s-8.4023-18-18-18z"/>
            <path d="m741.6 928.8h-333.6c-9.6016 0-18 8.3984-18 18s8.3984 18 18 18h333.6c9.6016 0 18-8.3984 18-18s-8.4023-18-18-18z"/>
            <path d="m241.2 529.2c3.6016 4.8008 8.3984 7.1992 14.398 7.1992s10.801-2.3984 14.398-7.1992l79.199-103.2c6-8.3984 4.8008-19.199-3.6016-25.199-8.3984-6-19.199-4.8008-25.199 3.6016l-64.801 84-25.195-32.402c-6-8.3984-16.801-9.6016-25.199-3.6016-8.3984 6-9.6016 16.801-3.6016 25.199z"/>
            <path d="m241.2 769.2c3.6016 4.8008 8.3984 7.1992 14.398 7.1992s10.801-2.3984 14.398-7.1992l79.199-103.2c6-8.3984 4.8008-19.199-3.6016-25.199-8.3984-6-19.199-4.8008-25.199 3.6016l-64.801 84-25.195-32.402c-6-8.3984-16.801-9.6016-25.199-3.6016-8.3984 6-9.6016 16.801-3.6016 25.199z"/>
            </g>
          </svg>

          <div class="tooltip">
            <span> Required hardware complete the Demo </span>
          </div>
        </div>
        <div class=hardware-content>
          <div class="symbol-wifi has-tooltip">
            <svg width="20px" height="20px" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" version="1.1" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path d="m11.928 17.074c0.61689 8.3e-5 1.1986 0.28706 1.5741 0.77649 0.37541 0.48944 0.50192 1.1256 0.34216 1.7214-0.15969 0.59581-0.58746 1.0835-1.1574 1.3195-0.5699 0.23601-1.2172 0.19348-1.7514-0.11496-0.53416-0.30851-0.89452-0.84784-0.97498-1.4594-0.08038-0.61158 0.12816-1.2258 0.56437-1.662 0.37173-0.37267 0.87672-0.58185 1.4032-0.58107zm0.37111 1.6133c-0.11535-0.11551-0.27792-0.17085-0.43981-0.14969-0.16187 0.02122-0.3047 0.11653-0.38642 0.25787-0.08172 0.14134-0.09302 0.31265-0.03061 0.46352 0.06244 0.15087 0.19145 0.26412 0.34919 0.30642 0.15766 0.0423 0.32608 0.0088 0.45566-0.09061 0.12956-0.09935 0.20542-0.25335 0.20542-0.41663 1.65e-4 -0.13916-0.05502-0.27256-0.15344-0.37088zm-10.8-10.067c-0.18232 0.1856-0.4498 0.25983-0.70165 0.19473-0.25193-0.065092-0.44995-0.25959-0.51949-0.51028-0.069621-0.25069-1.6453e-4 -0.51941 0.18217-0.705 0.047618-0.048311 0.095381-0.096072 0.14331-0.14331v-8.05e-5c3.0232-2.9655 7.089-4.6266 11.324-4.6266 4.2348 0 8.3006 1.6613 11.324 4.6266 0.04793 0.047457 0.09576 0.095219 0.14329 0.14329v8.54e-5c0.18232 0.1856 0.25179 0.45431 0.18217 0.705-0.06954 0.2507-0.26764 0.44518-0.51949 0.51028-0.25185 0.065082-0.51933-0.00913-0.70165-0.19473-0.04192-0.042443-0.08389-0.084532-0.12604-0.12629-2.7523-2.6949-6.4513-4.2041-10.303-4.2041-3.852 0-7.5508 1.5092-10.303 4.2041-0.04207 0.041736-0.084057 0.083816-0.12605 0.12629zm3.6652 3.6652c0.041923-0.0423 0.083977-0.08431 0.12629-0.12605 1.7775-1.7278 4.1587-2.6945 6.6377-2.6945 2.479 0 4.8602 0.96663 6.6377 2.6945 0.04244 0.04154 0.08452 0.08359 0.12629 0.12605 0.13448 0.14127 0.32009 0.2226 0.51511 0.22572 0.19504 0.0032 0.38314-0.07204 0.52222-0.20878 0.13908-0.13682 0.21745-0.32366 0.21745-0.51871 0-0.19504-0.0782-0.38196-0.21721-0.51887-0.04746-0.04815-0.09522-0.09585-0.14329-0.14306-2.0484-1.9982-4.7967-3.1167-7.6583-3.1167-2.8616 0-5.6099 1.1185-7.6583 3.1167-0.048311 0.04721-0.096075 0.09491-0.14331 0.14306-0.139 0.1369-0.21729 0.32382-0.21721 0.51887 0 0.19504 0.078363 0.38189 0.21745 0.51871 0.13908 0.13674 0.32718 0.21197 0.52223 0.20878 0.19504-0.0032 0.38065-0.08444 0.51511-0.22572zm10.944 2.6124h8.5e-5c0.18021 0.18739 0.24686 0.45673 0.17467 0.70657-0.07219 0.24983-0.27215 0.44214-0.52457 0.50458-0.25241 0.06235-0.51895-0.01468-0.69923-0.20198-0.54181-0.5635-1.2257-0.97028-1.9795-1.1776-0.75372-0.20721-1.5495-0.20721-2.3031 0-0.75379 0.2073-1.4376 0.61408-1.9794 1.1776-0.18029 0.18739-0.44682 0.26434-0.69923 0.20198-0.25241-0.06244-0.45237-0.25475-0.52456-0.50458-0.072185-0.24984-0.00549-0.51917 0.17467-0.70657 0.72327-0.75254 1.6363-1.2958 2.6426-1.5727 1.0063-0.27677 2.0688-0.27677 3.0752 0 1.0063 0.27682 1.9193 0.82013 2.6426 1.5727zm-4.1801 4.6842c0.16289-2.45e-4 0.31641-0.07609 0.41545-0.20542 0.09905-0.12932 0.13229-0.29736 0.08999-0.45463-0.04221-0.15734-0.15532-0.28596-0.3058-0.34826-0.15056-0.0622-0.3214-0.05096-0.46244 0.03061-0.14103 0.08148-0.23617 0.22392-0.25733 0.3854-0.02123 0.16148 0.03382 0.32366 0.14898 0.43887 0.09841 0.09841 0.23195 0.1536 0.37112 0.15344z" fill-rule="evenodd" stroke-width=".039961"/>
            </svg>
            <div class="tooltip">
              <span> Cool Tooltip </span>
            </div>
          </div>
          <div class="symbol-usb-stick has-tooltip">
            <svg width="20px" height="20px" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" version="1.1" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <g transform="matrix(.025362 0 0 .025362 -3.2174 -3.218)">
                <path d="m742.97 1068.8h-285.94c-17.406 0-34.098-6.9141-46.402-19.223-12.309-12.305-19.223-28.996-19.223-46.402v-558.38c0-17.406 6.9141-34.098 19.223-46.402 12.305-12.309 28.996-19.223 46.402-19.223h285.94c17.406 0 34.098 6.9141 46.402 19.223 12.309 12.305 19.223 28.996 19.223 46.402v558.38c0 17.406-6.9141 34.098-19.223 46.402-12.305 12.309-28.996 19.223-46.402 19.223zm-285.94-652.12c-7.4609 0-14.613 2.9648-19.887 8.2383-5.2734 5.2734-8.2383 12.426-8.2383 19.887v558.38c0 7.4609 2.9648 14.613 8.2383 19.887 5.2734 5.2734 12.426 8.2383 19.887 8.2383h285.94c7.4609 0 14.613-2.9648 19.887-8.2383 5.2734-5.2734 8.2383-12.426 8.2383-19.887v-558.38c0-7.4609-2.9648-14.613-8.2383-19.887-5.2734-5.2734-12.426-8.2383-19.887-8.2383z"/>
                <path d="m712.5 416.62h-225c-4.9727 0-9.7422-1.9766-13.258-5.4922-3.5156-3.5156-5.4922-8.2852-5.4922-13.258v-201c0-17.406 6.9141-34.098 19.223-46.402 12.305-12.309 28.996-19.223 46.402-19.223h131.25c17.406 0 34.098 6.9141 46.402 19.223 12.309 12.305 19.223 28.996 19.223 46.402v201c0 4.9727-1.9766 9.7422-5.4922 13.258-3.5156 3.5156-8.2852 5.4922-13.258 5.4922zm-206.25-37.5h187.5v-182.25c0-7.4609-2.9648-14.613-8.2383-19.887-5.2734-5.2734-12.426-8.2383-19.887-8.2383h-131.25c-7.4609 0-14.613 2.9648-19.887 8.2383-5.2734 5.2734-8.2383 12.426-8.2383 19.887z"/>
                <path d="m561.66 345.38c-4.9727 0-9.7422-1.9766-13.258-5.4922-3.5156-3.5156-5.4922-8.2852-5.4922-13.258v-105.47c0-6.6992 3.5742-12.887 9.375-16.238 5.8008-3.3477 12.949-3.3477 18.75 0 5.8008 3.3516 9.375 9.5391 9.375 16.238v105.47c0 4.9727-1.9766 9.7422-5.4922 13.258-3.5156 3.5156-8.2852 5.4922-13.258 5.4922z"/>
                <path d="m638.34 345.38c-4.9727 0-9.7422-1.9766-13.258-5.4922-3.5156-3.5156-5.4922-8.2852-5.4922-13.258v-105.47c0-6.6992 3.5742-12.887 9.375-16.238 5.8008-3.3477 12.949-3.3477 18.75 0 5.8008 3.3516 9.375 9.5391 9.375 16.238v105.47c0 4.9727-1.9766 9.7422-5.4922 13.258-3.5156 3.5156-8.2852 5.4922-13.258 5.4922z"/>
              </g>
            </svg>
            <div class="tooltip">
              <span> Cool Tooltip </span>
            </div>
          </div>
          <div class="symbol-phone has-tooltip">
            <svg width="20px" height="20px" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" version="1.1" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path d="m7.408 1.8977c-0.75525 0-1.3776 0.62234-1.3776 1.3776v17.449c0 0.75525 0.62233 1.3776 1.3776 1.3776h9.184c0.75525 0 1.3776-0.62233 1.3776-1.3776v-17.449c0-0.75525-0.62233-1.3776-1.3776-1.3776zm0 0.91834h9.184c0.26228 0 0.45915 0.19688 0.45915 0.45928v0.45915h-10.102v-0.45915c0-0.2624 0.19677-0.45928 0.45915-0.45928zm-0.45915 1.8368h10.102v12.857h-10.102zm0 13.776h10.102v2.2959c0 0.26239-0.19689 0.45928-0.45915 0.45928h-9.184c-0.2624 0-0.45916-0.19689-0.45916-0.45928zm5.0509 0.68881c-0.38038 0-0.68869 0.30831-0.68869 0.6888 0 0.38038 0.30831 0.68881 0.68869 0.68881 0.38047 0 0.68881-0.30844 0.68881-0.68881 0-0.38046-0.30831-0.6888-0.68881-0.6888z" stroke-width=".060763"/>
            </svg>
            <div class="tooltip">
              <span> Cool Tooltip </span>
            </div>
            </div>
        </div>
      </div>
    </div>
    <div class="card-buttons">
      <button type="button" class="wp-block-button__link has-background wp-element-button button learning-button">
          <svg
              xmlns="http://www.w3.org/2000/svg"
              width="15px"
              height="15px"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
              class="feather feather-book-open"
              >
              <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
              <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
          </svg>
        <span class=learn-button-text> Lehrmaterial </span>
        </a>
      </button>
      <button type="button" class="wp-block-button__link has-background wp-element-button button stop-demo-button">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="20px"
          height="20px"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="mr-50 feather feather-play-circle">
          <circle cx="12" cy="12" r="10"></circle>
          <rect x="9" y="9" width="6" height="6"></rect>
        </svg>
        <span class="align-middle stop-button-text">Demo stoppen</span>
      </button>
      <button type="button" class="wp-block-button__link has-background wp-element-button button start-demo-button">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="20px"
          height="20px"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="mr-50 feather feather-play-circle start-button-icon">
          <circle cx="12" cy="12" r="10"></circle>
          <polygon points="10 8 16 12 10 16 10 8"></polygon>
        </svg>
        <div class="start-button-loading ld-ext-right running">
          <div class="ld ld-ring ld-spin"></div>
        </div>
        <span class="align-middle start-button-text">Demo starten</span>
      </button>
    </div>
  </div>
</div>`;

function create_card() {
	const template = document.createElement('template');
	template.innerHTML = CARD_TEMPLATE;
	return template.content.childNodes[0];
}

class DemoCard {
	constructor(name, title, description, level, time, guide, instructor_id, hardware) {
		this.name = name;
		const container = document.querySelector('#demo_container');
		this.card = document.createElement('div');
		this.card = create_card();
		this.card.id = name;
		this.enabled = true;
		this.guide = guide;
		this.description = description;

		this.set_title(title);
    this.set_instructor(instructor_id);
		this.set_description(description);
		this.set_level(level);
		this.set_time(time);

		container.append(this.card);

		const link = this.card.querySelector('.learning-button');
		const stop_button = this.card.querySelector('.stop-demo-button');
		link.addEventListener('click', e => {
			window.location = `../courses/${name}`;
		});
    // Language
    link.querySelector(".learn-button-text").innerText = common_translations["learn_button"];
    this.card.querySelector(".start-button-text").innerText = common_translations["start_button"];
    stop_button.querySelector(".stop-button-text").innerText = common_translations["stop_button"];

    this.card.querySelector(".card-hardware .tooltip > span").innerHTML = common_translations["tooltip_hardware"];
    this.card.querySelector(".card-time .tooltip > span").innerHTML = common_translations["tooltip_time"];
    this.card.querySelector(".card-difficulty .tooltip > span").innerHTML = common_translations["tooltip_difficulty"];

    for(let h of hardware) {
      let sym = this.card.querySelector(`.symbol-${h}`);
      if(sym !== undefined) {
        this.card.querySelector('.card-hardware').style.display = 'flex';
        sym.style.display = 'flex';
        let tooltip = sym.querySelector(".tooltip > span");
        tooltip.innerHTML = common_translations[h];
      }
    }



		this.add_start_button_listener();

		stop_button.addEventListener('click', e => {
			this.set_demo_state("unknown", "waiting", common_translations["start_waiting"], "");
			const xhr_req = new XMLHttpRequest();
			xhr_req.open('GET', `http://127.0.0.1:5000/orchestration/stop/demo/${this.name}`);
      xhr_req.send();
		});
	}

	add_start_button_listener() {
		const start_button = this.card.querySelector('.start-demo-button');
		start_button.onclick = e => {
			this.set_demo_state("unknown", "waiting", common_translations["start_waiting"], "");
			const xhr = new XMLHttpRequest();
			xhr.open('POST', `http://127.0.0.1:5000/orchestration/start/demo/${this.name}`);
      xhr.setRequestHeader("Content-Type", "application/json");
      let lang = "de";
      if(typeof(get_lang) == "function") {
        lang = get_lang().split('_')[0];
      }
      const json_data = JSON.stringify({ "language": lang });
      xhr.send(json_data);
		};
	}

	set_title(title) {
		this.card.querySelector('.card-title').innerText = title;
	}

	set_instructor(id) {
		let author_div = this.card.querySelector('.masteriyo-course-author');
    if(typeof(get_instructor) == "function") {
      let author_data = get_instructor(id);
      author_div.querySelector("img").src = author_data[1];
      author_div.querySelector(".masteriyo-course-author--name").innerText = author_data[0];
    }
	}

	set_description(desc) {
		this.card.querySelector('.card-text').innerHTML = desc;
	}

  set_guide(guide) {
		let desc_obj = this.card.querySelector('.card-text');
    let desc_content = ""
    let guide_objects = { "guide_intro": guide.guide_intro,
                          "guide_task": guide.guide_task,
                          "guide_goal": guide.guide_goal,
                          "guide_req": guide.guide_req}
    console.log("Setting guide!")
    console.log(guide_objects)
    for(let [key, val] of Object.entries(guide_objects)) {
      if(val.length > 0) {
        desc_content += `<h4> ${common_translations[key]} </h4><div>${val}</div>`
      }
    }
    desc_obj.innerHTML = desc_content;
  }

	set_level(lvl) {
		this.card.querySelector('.level-text').innerText = lvl;
	}

	set_time(time) {
		this.card.querySelector('.time-text').innerText = `${time}min`;
	}

	set_demo_state(old_state, state, translation, extra_state) {
		console.log(`demo ${this.name} changed from ${old_state} to ${state} and extra state ${extra_state}`);

		const start_button = this.card.querySelector('.start-demo-button');
		const button_text = start_button.querySelector('.start-button-text');
		const possible_classes = ['button-waiting', 'button-starting', 'button-ready', 'button-running', 'button-offline', 'button-stopping', 'button-error'];

		let i = 0;
		for (i in possible_classes) {
			start_button.classList.remove(possible_classes[i]);
		}

		start_button.classList.add(`button-${state}`);
    if (state === 'error') {
      button_text.innerText = translation;
      start_button.onclick = "";
    }


		// Change start button in these states
		if (state === 'waiting' || state === 'starting' || state === 'ready' || state === 'running' || state === 'stopping') {
			this.card.classList.add('large-card');
			this.card.parentNode.classList.add('hide-small');
			this.set_guide(this.guide);
			const button_image = start_button.querySelector('.start-button-icon');
			button_text.innerText = translation;
			if (extra_state !== '') {
				button_text.innerText = extra_state;
			}

			console.log(`button-${state}`);
			start_button.onclick = "";

			if (state === 'ready') {
				start_button.addEventListener('click', e => {
					const xhr = new XMLHttpRequest();
					xhr.open('GET', `http://127.0.0.1:5000/orchestration/enter/demo/${this.name}`);
					xhr.send();
				});
			}
		}

		if (state == 'offline') {
			button_text.innerText = common_translations.start_button;
			this.card.classList.remove('large-card');
			if (this.card.parentNode.querySelector('.large-card') === null) {
				this.card.parentNode.classList.remove('hide-small');
			}

			this.add_start_button_listener();
			this.set_description(this.description);
		}
	}
}

function create_loading_page() {
	const container = document.querySelector('#demo_container');
	const text = document.createElement('div');
	const spinning = document.createElement('div');
	text.innerText = 'Loading Demos...';
	container.append(text);
  container.append(spinning);
  container.classList.add("running");
}

create_loading_page();
const xhr = new XMLHttpRequest();
xhr.open('POST', 'http://127.0.0.1:5000/orchestration/getdemos');
xhr.setRequestHeader("Content-Type", "application/json");
let lang = "de";
if(typeof(get_lang) == "function") {
  lang = get_lang().split('_')[0];
}
const json_data = JSON.stringify({ "language": lang });
xhr.send(json_data);
xhr.addEventListener('load', () => {
	const container = document.querySelector('#demo_container');
	while (container.firstChild) {
		container.firstChild.remove();
	}
  container.classList.remove("running");

	if (xhr.status == 200) {
		const data = JSON.parse(xhr.response);
		console.log(data);
    common_translations = data.common_translations;
		for (const d of data.demos) {
			console.log(d);
			demo = new DemoCard(d.name, d.title, d.description, d.level, d.time, d.guide, d.instructor_id, d.hardware);
			demo_dict[d.name] = demo;
		}
	} else {
		const text = document.createElement('div');
		text.innerText = 'Error while loading demos';
		container.append(text);
	}

	start_status_stream();
});

xhr.onerror = function () {
	const container = document.querySelector('#demo_container');
	while (container.firstChild) {
		container.firstChild.remove();
	}

	const text = document.createElement('div');
	text.innerText = 'Error while loading demos';
	container.append(text);
  container.classList.remove("running");
};

/*

 {
  "name": "demo_name",
  "state_id": "starting",
  "old_state_id": "offline",
  "new_state": "Starting demo"
  "extra_state": "Starting container"
  }

 */
function start_status_stream() {
	const eventSource = new EventSource('http://127.0.0.1:5000/orchestration/status/stream');
	eventSource.onmessage = e => {
		const data = JSON.parse(e.data);
		const demo = demo_dict[data.name];
		console.log('Got new status data:');
		console.log(data);
		if (demo !== undefined) {
			demo.set_demo_state(data.old_state_id, data.state_id, data.state, data.extra_state);
		}
	};
  eventSource.onerror = e => {
    setTimeout(() => {
      start_status_stream();
    }, 1);
  }
}
