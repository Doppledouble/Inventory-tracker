import { ref, computed } from "vue";

// This if for Filter & Sort function
export function useTableControls(data, filterFields, defaultSortKey = "id") {

  // ── Filters ──────────────────────────────────────────────
    const filters = ref(Object.fromEntries(filterFields.map((f) => [f.key, ""])));

    const filteredData = computed(() => {
    return data.value.filter((row) => {
        return filterFields.every(({ key, resolve, type = "text" }) => {
        const filterVal = filters.value[key];

        if (filterVal === "" || filterVal === null) return true;

        const cellVal = resolve ? resolve(row) : row[key];

        if (type === "number") {
            return Number(cellVal) === Number(filterVal);
        }

        if (type === "date") {
            return String(cellVal)
            .toLowerCase()
            .includes(String(filterVal).toLowerCase());
        }

        return String(cellVal ?? "")
            .toLowerCase()
            .includes(String(filterVal).toLowerCase());
        });
    });
    });

    // ── Sorting ──────────────────────────────────────────────
    const sortKey = ref(defaultSortKey);
    const sortOrder = ref("desc");

    const toggleSort = (key) => {
        if (sortKey.value === key) {
        sortOrder.value = sortOrder.value === "asc" ? "desc" : "asc";
        } else {
        sortKey.value = key;
        sortOrder.value = "asc";
        }
    };

    const getSortIcon = (key) => {
        if (sortKey.value !== key) return "ti-arrows-sort";
        return sortOrder.value === "asc" ? "ti-arrow-up" : "ti-arrow-down";
    };

    const sortedData = computed(() => {
    const field = filterFields.find((f) => f.key === sortKey.value);

    return [...filteredData.value].sort((a, b) => {
        let aVal = field?.resolve ? field.resolve(a) : a[sortKey.value];
        let bVal = field?.resolve ? field.resolve(b) : b[sortKey.value];

        const type = field?.type ?? "text";

        if (type === "text") {
        aVal = String(aVal ?? "").toLowerCase();
        bVal = String(bVal ?? "").toLowerCase();
        }

        if (type === "number") {
        aVal = Number(aVal);
        bVal = Number(bVal);
        }

        if (type === "date") {
        aVal = new Date(aVal).getTime();
        bVal = new Date(bVal).getTime();
        }

        if (aVal < bVal) return sortOrder.value === "asc" ? -1 : 1;
        if (aVal > bVal) return sortOrder.value === "asc" ? 1 : -1;
        return 0;
    });
    });

    return {
        filters,
        sortKey,
        sortOrder,
        toggleSort,
        getSortIcon,
        result: sortedData, // final filtered + sorted data
    };
}