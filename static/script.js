// Write Javascript (using axios and jQuery) that:

// queries the API to get the cupcakes and adds to the page
// handles form submission to both let the API know about the new cupcake and updates the list on the page to show it

const BASE_URL = "http://127.0.0.1:5000/api";

/** generate HTML for a cupcake */
function generateCupcakeHTML(cupcake) {
	return `
    <div data-cupcake-id="${cupcake.id}">
        <li>${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}</li>
        <div><img src="${cupcake.image}" alt="image of ${cupcake.flavor} cupcake" class="cupcake-img" /></div> 
    </div>
    `;
}

/** put all cupcakes on page */
async function showCupcakes() {
	const response = await axios.get(`${BASE_URL}/cupcakes`);

	for (let cupcakeData of response.data.cupcakes) {
		let newCupcake = $(generateCupcakeHTML(cupcakeData));
		$("#cupcakes-list").append(newCupcake);
	}
}

/** handle form adding new cupcake */
$("#new-cupcake-form").on("submit", async (evt) => {
	evt.preventDefault();

	let flavor = $("#flavor").val();
	let size = $("#size").val();
	let rating = $("#rating").val();
	let image = $("#image").val();

	const newCupcakeResponse = await axios.post(`${BASE_URL}/cupcakes`, {
		flavor,
		size,
		rating,
		image,
    });
    
    let newCupcake = $(generateCupcakeHTML(newCupcakeResponse.data.cupcake));
    $("#cupcakes-list").append(newCupcake);
    $("#new-cupcake-form").trigger("reset");
});

$(showCupcakes);
